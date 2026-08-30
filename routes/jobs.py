from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort
)

from extensions import db
from models.job import JobOpening
from utils.decorators import role_required


jobs_bp = Blueprint(
    "jobs",
    __name__,
    url_prefix="/jobs"
)


@jobs_bp.route("/")
@role_required("recruiter")
def job_list():

    status = request.args.get("status", "active")

    if status == "archived":
        jobs = (
            JobOpening.query
            .filter_by(status="archived")
            .order_by(JobOpening.created_at.desc())
            .all()
        )

    elif status == "all":
        jobs = (
            JobOpening.query
            .order_by(JobOpening.created_at.desc())
            .all()
        )

    else:
        jobs = (
            JobOpening.query
            .filter(JobOpening.status.in_(["open", "closed"]))
            .order_by(JobOpening.created_at.desc())
            .all()
        )

    return render_template(
        "jobs/list.html",
        jobs=jobs,
        selected_status=status
    )


@jobs_bp.route("/create", methods=["GET", "POST"])
@role_required("recruiter")
def create_job():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        department = request.form.get("department", "").strip()
        description = request.form.get("description", "").strip()

        if not title:
            flash("Job title is required.", "error")
            return render_template("jobs/create.html")

        if not department:
            flash("Department is required.", "error")
            return render_template("jobs/create.html")

        job = JobOpening(
            title=title,
            department=department,
            description=description,
            status="open"
        )

        db.session.add(job)
        db.session.commit()

        flash("Job opening created successfully.", "success")

        return redirect(url_for("jobs.job_list"))

    return render_template("jobs/create.html")


@jobs_bp.route("/<int:job_id>/edit", methods=["GET", "POST"])
@role_required("recruiter")
def edit_job(job_id):

    job = db.session.get(JobOpening, job_id)

    if not job:
        abort(404)

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        department = request.form.get("department", "").strip()
        description = request.form.get("description", "").strip()

        if not title:
            flash("Job title is required.", "error")

            return render_template(
                "jobs/edit.html",
                job=job
            )

        if not department:
            flash("Department is required.", "error")

            return render_template(
                "jobs/edit.html",
                job=job
            )

        job.title = title
        job.department = department
        job.description = description

        db.session.commit()

        flash("Job opening updated successfully.", "success")

        return redirect(url_for("jobs.job_list"))

    return render_template(
        "jobs/edit.html",
        job=job
    )


@jobs_bp.route("/<int:job_id>/close", methods=["POST"])
@role_required("recruiter")
def close_job(job_id):

    job = db.session.get(JobOpening, job_id)

    if not job:
        abort(404)

    if job.status == "archived":
        flash("Archived jobs cannot be closed.", "error")

        return redirect(url_for("jobs.job_list"))

    job.status = "closed"

    db.session.commit()

    flash("Job opening closed successfully.", "success")

    return redirect(url_for("jobs.job_list"))


@jobs_bp.route("/<int:job_id>/open", methods=["POST"])
@role_required("recruiter")
def open_job(job_id):

    job = db.session.get(JobOpening, job_id)

    if not job:
        abort(404)

    if job.status == "archived":
        flash("Restore the job before opening it.", "error")

        return redirect(url_for("jobs.job_list"))

    job.status = "open"

    db.session.commit()

    flash("Job opening reopened successfully.", "success")

    return redirect(url_for("jobs.job_list"))


@jobs_bp.route("/<int:job_id>/archive", methods=["POST"])
@role_required("recruiter")
def archive_job(job_id):

    job = db.session.get(JobOpening, job_id)

    if not job:
        abort(404)

    if job.status == "archived":
        flash("Job is already archived.", "error")

        return redirect(url_for("jobs.job_list"))

    job.status = "archived"

    db.session.commit()

    flash("Job opening archived successfully.", "success")

    return redirect(url_for("jobs.job_list"))


@jobs_bp.route("/<int:job_id>/restore", methods=["POST"])
@role_required("recruiter")
def restore_job(job_id):

    job = db.session.get(JobOpening, job_id)

    if not job:
        abort(404)

    if job.status != "archived":
        flash("Only archived jobs can be restored.", "error")

        return redirect(url_for("jobs.job_list"))

    job.status = "closed"

    db.session.commit()

    flash("Job opening restored successfully.", "success")

    return redirect(
        url_for(
            "jobs.job_list",
            status="archived"
        )
    )