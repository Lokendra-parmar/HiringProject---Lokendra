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
from models.user import User

from sqlalchemy import or_

from utils.decorators import role_required
from utils.application_helpers import create_application_event

# to use pipeline
from utils.pipeline import (
    advance_application,
    reject_application,
    reinstate_application
)


applications_bp = Blueprint(
    "applications",
    __name__,
    url_prefix="/applications"
)


@applications_bp.route("/")
@role_required("recruiter")
def application_list():

    search = request.args.get(
        "search",
        ""
    ).strip()

    stage = request.args.get(
        "stage",
        ""
    ).strip()

    job_id = request.args.get(
        "job_id",
        ""
    ).strip()

    source = request.args.get(
        "source",
        ""
    ).strip()

    sort = request.args.get(
        "sort",
        "newest"
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:
        page = 1

    query = Application.query

    # -------------------------
    # SEARCH
    # -------------------------

    if search:

        search_pattern = f"%{search}%"

        query = query.filter(
            or_(
                Application.candidate_name.ilike(
                    search_pattern
                ),
                Application.candidate_email.ilike(
                    search_pattern
                )
            )
        )

    # -------------------------
    # FILTER BY STAGE
    # -------------------------

    if stage:

        query = query.filter(
            Application.stage == stage
        )

    # -------------------------
    # FILTER BY JOB
    # -------------------------

    if job_id:

        try:
            job_id_int = int(job_id)

            query = query.filter(
                Application.job_opening_id ==
                job_id_int
            )

        except ValueError:
            job_id = ""

    # -------------------------
    # FILTER BY SOURCE
    # -------------------------

    if source:

        query = query.filter(
            Application.source == source
        )

    # -------------------------
    # SORTING
    # -------------------------

    if sort == "oldest":

        query = query.order_by(
            Application.applied_at.asc()
        )

    elif sort == "name_asc":

        query = query.order_by(
            Application.candidate_name.asc()
        )

    elif sort == "name_desc":

        query = query.order_by(
            Application.candidate_name.desc()
        )

    else:

        # Default = newest
        sort = "newest"

        query = query.order_by(
            Application.applied_at.desc()
        )

    # -------------------------
    # PAGINATION
    # -------------------------

    pagination = query.paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    applications = pagination.items

    jobs = (
        JobOpening.query
        .order_by(JobOpening.title)
        .all()
    )

    sources = (
        db.session.query(
            Application.source
        )
        .filter(
            Application.source.isnot(None),
            Application.source != ""
        )
        .distinct()
        .order_by(
            Application.source
        )
        .all()
    )

    sources = [
        item[0]
        for item in sources
    ]

    stages = [
        "Applied",
        "Screening",
        "Interview",
        "Offer",
        "Hired",
        "Rejected"
    ]

    return render_template(
        "applications/list.html",
        applications=applications,
        pagination=pagination,
        jobs=jobs,
        stages=stages,
        sources=sources,
        search=search,
        selected_stage=stage,
        selected_job=job_id,
        selected_source=source,
        selected_sort=sort
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

    if current_user.role == "interviewer":

        from utils.interviewer import is_assigned_interviewer

        if not is_assigned_interviewer(
            application.id,
            current_user.id
        ):
            abort(403)

    interviewers = []

    if current_user.role == "recruiter":

        interviewers = (
            User.query
            .filter_by(role="interviewer")
            .order_by(User.name)
            .all()
        )

    return render_template(
        "applications/detail.html",
        application=application,
        interviewers=interviewers
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


# pipeline routes advance
@applications_bp.route(
    "/<int:application_id>/advance",
    methods=["POST"]
)
@role_required("recruiter")
def advance(application_id):

    application = db.session.get(
        Application,
        application_id
    )

    if not application:
        abort(404)

    try:

        advance_application(
            application,
            current_user.id
        )

        db.session.commit()

        flash(
            "Application advanced successfully.",
            "success"
        )

    except ValueError as error:

        db.session.rollback()

        flash(
            str(error),
            "error"
        )

    return redirect(
        url_for(
            "applications.application_detail",
            application_id=application.id
        )
    )

#pipeline routes reject
@applications_bp.route(
    "/<int:application_id>/reject",
    methods=["POST"]
)
@role_required("recruiter")
def reject(application_id):

    application = db.session.get(
        Application,
        application_id
    )

    if not application:
        abort(404)

    try:

        reject_application(
            application,
            current_user.id
        )

        db.session.commit()

        flash(
            "Application rejected.",
            "success"
        )

    except ValueError as error:

        db.session.rollback()

        flash(
            str(error),
            "error"
        )

    return redirect(
        url_for(
            "applications.application_detail",
            application_id=application.id
        )
    )

#pipeline routes reinstate
@applications_bp.route(
    "/<int:application_id>/reinstate",
    methods=["POST"]
)
@role_required("recruiter")
def reinstate(application_id):

    application = db.session.get(
        Application,
        application_id
    )

    if not application:
        abort(404)

    try:

        reinstate_application(
            application,
            current_user.id
        )

        db.session.commit()

        flash(
            "Application reinstated successfully.",
            "success"
        )

    except ValueError as error:

        db.session.rollback()

        flash(
            str(error),
            "error"
        )

    return redirect(
        url_for(
            "applications.application_detail",
            application_id=application.id
        )
    )

