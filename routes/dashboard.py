from datetime import datetime, timedelta

from flask import Blueprint, render_template
from flask_login import current_user

from sqlalchemy import func

from extensions import db
from models.job import JobOpening
from models.application import Application
from models.event import ApplicationEvent
from models.interview import InterviewSchedule
from utils.decorators import role_required


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
@role_required("recruiter", "interviewer")
def dashboard():

    # Interviewers have their own simpler landing page.
    if current_user.role == "interviewer":

        return render_template(
            "dashboard.html",
            interviewer_view=True
        )

    now = datetime.utcnow()

    # ------------------------------------
    # HEADLINE METRICS
    # ------------------------------------

    open_positions = (
        JobOpening.query
        .filter_by(status="open")
        .count()
    )

    active_applications = (
        Application.query
        .filter(
            Application.stage.notin_(
                ["Hired", "Rejected"]
            )
        )
        .count()
    )

    # Beginning of current week: Monday 00:00
    week_start = (
        now -
        timedelta(days=now.weekday())
    ).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    week_end = week_start + timedelta(days=7)

    interviews_this_week = (
        InterviewSchedule.query
        .filter(
            InterviewSchedule.scheduled_at >= week_start,
            InterviewSchedule.scheduled_at < week_end
        )
        .count()
    )

    month_start = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    hires_this_month = (
        Application.query
        .join(
            ApplicationEvent,
            Application.id ==
            ApplicationEvent.application_id
        )
        .filter(
            ApplicationEvent.event_type == "STAGE_CHANGED",
            ApplicationEvent.new_stage == "Hired",
            ApplicationEvent.created_at >= month_start
        )
        .count()
    )

    # ------------------------------------
    # APPLICATIONS BY STAGE
    # ------------------------------------

    stage_results = (
        db.session.query(
            Application.stage,
            func.count(Application.id)
        )
        .group_by(Application.stage)
        .all()
    )

    stage_counts = {
        stage: count
        for stage, count in stage_results
    }

    # ------------------------------------
    # APPLICATIONS BY JOB OPENING
    # ------------------------------------

    job_results = (
        db.session.query(
            JobOpening.title,
            func.count(Application.id)
        )
        .outerjoin(
            Application,
            JobOpening.id ==
            Application.job_opening_id
        )
        .filter(
            JobOpening.status != "archived"
        )
        .group_by(
            JobOpening.id,
            JobOpening.title
        )
        .order_by(
            JobOpening.title
        )
        .all()
    )

    job_labels = [
        title
        for title, count in job_results
    ]

    job_counts = [
        count
        for title, count in job_results
    ]

    # ------------------------------------
    # APPLICATIONS PER WEEK — LAST QUARTER
    # ------------------------------------

    quarter_start = now - timedelta(days=90)

    recent_applications = (
        Application.query
        .filter(
            Application.applied_at >= quarter_start
        )
        .order_by(
            Application.applied_at
        )
        .all()
    )

    weekly_counts = {}

    # Build 13 weekly buckets.
    for i in range(13):

        bucket_start = (
            quarter_start +
            timedelta(weeks=i)
        )

        label = bucket_start.strftime(
            "%d %b"
        )

        weekly_counts[label] = 0

    for application in recent_applications:

        if not application.applied_at:
            continue

        days_since_start = (
            application.applied_at -
            quarter_start
        ).days

        week_index = days_since_start // 7

        if 0 <= week_index < 13:

            bucket_start = (
                quarter_start +
                timedelta(weeks=week_index)
            )

            label = bucket_start.strftime(
                "%d %b"
            )

            weekly_counts[label] += 1

    weekly_labels = list(
        weekly_counts.keys()
    )

    weekly_values = list(
        weekly_counts.values()
    )

    return render_template(
        "dashboard.html",

        interviewer_view=False,

        open_positions=open_positions,
        active_applications=active_applications,
        interviews_this_week=interviews_this_week,
        hires_this_month=hires_this_month,

        stage_counts=stage_counts,

        job_labels=job_labels,
        job_counts=job_counts,

        weekly_labels=weekly_labels,
        weekly_values=weekly_values
    )
    return render_template("dashboard.html")
from utils.decorators import role_required


@dashboard_bp.route("/recruiter-test")
@role_required("recruiter")
def recruiter_test():

    return "Recruiter access granted!"