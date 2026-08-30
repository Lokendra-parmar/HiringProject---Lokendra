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
from models.job import JobOpening
from utils.decorators import role_required
from utils.application_helpers import create_application_event


applications_bp = Blueprint(
    "applications",
    __name__,
    url_prefix="/applications"
)


@applications_bp.route("/")
@role_required("recruiter")
def application_list():

    applications = (
        Application.query
        .order_by(Application.applied_at.desc())
        .all()
    )

    return render_template(
        "applications/list.html",
        applications=applications
    )


@applications_bp.route("/create", methods=["GET", "POST"])
@role_required("recruiter")
def create_application():

    jobs = (
        JobOpening.query
        .filter_by(status="open")
        .order_by(JobOpening.title)
        .all()
    )

    if request.method == "POST":

        candidate_name = request.form.get(
            "candidate_name",
            ""
        ).strip()

        candidate_email = request.form.get(
            "candidate_email",
            ""
        ).strip().lower()

        source = request.form.get(
            "source",
            ""
        ).strip()

        notes = request.form.get(
            "notes",
            ""
        ).strip()

        job_opening_id = request.form.get(
            "job_opening_id"
        )

        if not candidate_name:
            flash(
                "Candidate name is required.",
                "error"
            )

            return render_template(
                "applications/create.html",
                jobs=jobs
            )

        if not candidate_email:
            flash(
                "Candidate email is required.",
                "error"
            )

            return render_template(
                "applications/create.html",
                jobs=jobs
            )

        if not job_opening_id:
            flash(
                "Please select a job opening.",
                "error"
            )

            return render_template(
                "applications/create.html",
                jobs=jobs
            )

        job = db.session.get(
            JobOpening,
            int(job_opening_id)
        )

        if not job:
            abort(404)

        if job.status != "open":
            flash(
                "Applications can only be added to open jobs.",
                "error"
            )

            return render_template(
                "applications/create.html",
                jobs=jobs
            )

        application = Application(
            job_opening_id=job.id,
            candidate_name=candidate_name,
            candidate_email=candidate_email,
            source=source,
            notes=notes,
            stage="Applied"
        )

        db.session.add(application)

        # We need the application ID before creating the event.
        db.session.flush()

        create_application_event(
            application=application,
            event_type="APPLICATION_CREATED",
            actor_id=current_user.id,
            new_stage="Applied",
            message="Application created."
        )

        db.session.commit()

        flash(
            "Application created successfully.",
            "success"
        )

        return redirect(
            url_for(
                "applications.application_detail",
                application_id=application.id
            )
        )

    return render_template(
        "applications/create.html",
        jobs=jobs
    )


@applications_bp.route("/<int:application_id>")
@role_required("recruiter", "interviewer")
def application_detail(application_id):

    application = db.session.get(
        Application,
        application_id
    )

    if not application:
        abort(404)

    return render_template(
        "applications/detail.html",
        application=application
    )


@applications_bp.route(
    "/<int:application_id>/edit",
    methods=["GET", "POST"]
)
@role_required("recruiter")
def edit_application(application_id):

    application = db.session.get(
        Application,
        application_id
    )

    if not application:
        abort(404)

    if request.method == "POST":

        candidate_name = request.form.get(
            "candidate_name",
            ""
        ).strip()

        candidate_email = request.form.get(
            "candidate_email",
            ""
        ).strip().lower()

        source = request.form.get(
            "source",
            ""
        ).strip()

        notes = request.form.get(
            "notes",
            ""
        ).strip()

        if not candidate_name:
            flash(
                "Candidate name is required.",
                "error"
            )

            return render_template(
                "applications/edit.html",
                application=application
            )

        if not candidate_email:
            flash(
                "Candidate email is required.",
                "error"
            )

            return render_template(
                "applications/edit.html",
                application=application
            )

        application.candidate_name = candidate_name
        application.candidate_email = candidate_email
        application.source = source
        application.notes = notes

        db.session.commit()

        flash(
            "Application updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "applications.application_detail",
                application_id=application.id
            )
        )

    return render_template(
        "applications/edit.html",
        application=application
    )