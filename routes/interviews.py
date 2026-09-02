from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort
)

from flask_login import current_user

from extensions import db

from models.application import Application
from models.user import User
from models.interview import (
    ApplicationInterviewer,
    Feedback,
    InterviewSchedule
)

from utils.decorators import role_required
from utils.interviewer import is_assigned_interviewer
from utils.events import create_application_event
from datetime import datetime

interviews_bp = Blueprint(
    "interviews",
    __name__,
    url_prefix="/interviews"
)

@interviews_bp.route(
    "/<int:application_id>/assign",
    methods=["POST"]
)
@role_required("recruiter")
def assign_interviewer(application_id):

    application = db.session.get(
        Application,
        application_id
    )

    if not application:
        abort(404)

    interviewer_id = request.form.get(
        "interviewer_id"
    )

    if not interviewer_id:
        flash(
            "Please select an interviewer.",
            "error"
        )

        return redirect(
            url_for(
                "applications.application_detail",
                application_id=application.id
            )
        )

    interviewer = db.session.get(
        User,
        int(interviewer_id)
    )

    if not interviewer:
        flash(
            "Interviewer not found.",
            "error"
        )

        return redirect(
            url_for(
                "applications.application_detail",
                application_id=application.id
            )
        )

    if interviewer.role != "interviewer":
        flash(
            "Selected user is not an interviewer.",
            "error"
        )

        return redirect(
            url_for(
                "applications.application_detail",
                application_id=application.id
            )
        )

    existing = (
        ApplicationInterviewer.query
        .filter_by(
            application_id=application.id,
            interviewer_id=interviewer.id
        )
        .first()
    )

    if existing:
        flash(
            "Interviewer is already assigned.",
            "error"
        )

        return redirect(
            url_for(
                "applications.application_detail",
                application_id=application.id
            )
        )

    assignment = ApplicationInterviewer(
        application_id=application.id,
        interviewer_id=interviewer.id
    )

    db.session.add(assignment)
    create_application_event(
        application_id=application.id,
        event_type="INTERVIEWER_ASSIGNED",
        actor_id=current_user.id,
        message=(
            f"{interviewer.name} was assigned "
            f"as an interviewer."
        )
    )
    db.session.commit()

    flash(
        f"{interviewer.name} assigned successfully.",
        "success"
    )

    return redirect(
        url_for(
            "applications.application_detail",
            application_id=application.id
        )
    )

@interviews_bp.route(
    "/<int:application_id>/remove/<int:interviewer_id>",
    methods=["POST"]
)
@role_required("recruiter")
def remove_interviewer(
    application_id,
    interviewer_id
):

    assignment = (
        ApplicationInterviewer.query
        .filter_by(
            application_id=application_id,
            interviewer_id=interviewer_id
        )
        .first()
    )

    if not assignment:
        abort(404)

    interviewer = db.session.get(
        User,
        interviewer_id
    )

    if interviewer:

        create_application_event(
            application_id=application_id,
            event_type="INTERVIEWER_REMOVED",
            actor_id=current_user.id,
            message=(
                f"{interviewer.name} was removed "
                f"from the interview panel."
            )
        )
    db.session.delete(assignment)

    db.session.commit()

    flash(
        "Interviewer removed.",
        "success"
    )

    return redirect(
        url_for(
            "applications.application_detail",
            application_id=application_id
        )
    )

@interviews_bp.route("/my-applications")
@role_required("interviewer")
def my_applications():

    applications = (
        Application.query
        .join(
            ApplicationInterviewer,
            Application.id ==
            ApplicationInterviewer.application_id
        )
        .filter(
            ApplicationInterviewer.interviewer_id ==
            current_user.id
        )
        .order_by(
            Application.applied_at.desc()
        )
        .all()
    )

    return render_template(
        "interviews/my_applications.html",
        applications=applications
    )


@interviews_bp.route(
    "/<int:application_id>/feedback",
    methods=["POST"]
)
@role_required("interviewer")
def add_feedback(application_id):

    application = db.session.get(
        Application,
        application_id
    )

    if not application:
        abort(404)

    if not is_assigned_interviewer(
        application.id,
        current_user.id
    ):
        abort(403)

    content = request.form.get(
        "content",
        ""
    ).strip()

    if not content:

        flash(
            "Feedback cannot be empty.",
            "error"
        )

        return redirect(
            url_for(
                "applications.application_detail",
                application_id=application.id
            )
        )

    feedback = Feedback(
        application_id=application.id,
        interviewer_id=current_user.id,
        content=content
    )

    db.session.add(feedback)

    create_application_event(
        application_id=application.id,
        event_type="INTERVIEW_FEEDBACK_SUBMITTED",
        actor_id=current_user.id,
        message=content
    )

    db.session.commit()

    flash(
        "Feedback added successfully.",
        "success"
    )

    return redirect(
        url_for(
            "applications.application_detail",
            application_id=application.id
        )
    )

@interviews_bp.route(
    "/<int:application_id>/schedule",
    methods=["POST"]
)
@role_required("recruiter")
def schedule_interview(application_id):

    application = db.session.get(
        Application,
        application_id
    )

    if not application:
        abort(404)

    scheduled_at = request.form.get(
        "scheduled_at",
        ""
    ).strip()

    notes = request.form.get(
        "notes",
        ""
    ).strip()

    if not scheduled_at:
        flash(
            "Interview date and time are required.",
            "error"
        )

        return redirect(
            url_for(
                "applications.application_detail",
                application_id=application.id
            )
        )

    try:

        interview_datetime = datetime.strptime(
            scheduled_at,
            "%Y-%m-%dT%H:%M"
        )

    except ValueError:

        flash(
            "Invalid interview date or time.",
            "error"
        )

        return redirect(
            url_for(
                "applications.application_detail",
                application_id=application.id
            )
        )

    interview = InterviewSchedule(
        application_id=application.id,
        scheduled_at=interview_datetime,
        notes=notes,
        created_by=current_user.id
    )

    db.session.add(interview)
    create_application_event(
        application_id=application.id,
            event_type="INTERVIEW_SCHEDULED",
            actor_id=current_user.id,
            message=(
                "Interview scheduled for "
                f"{interview_datetime.strftime('%d %b %Y, %I:%M %p')}."
            )       
    )
    db.session.commit()

    flash(
        "Interview scheduled successfully.",
        "success"
    )

    return redirect(
        url_for(
            "applications.application_detail",
            application_id=application.id
        )
    )