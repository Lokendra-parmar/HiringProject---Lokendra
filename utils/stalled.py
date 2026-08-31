from datetime import datetime, timedelta

from models.application import Application
from models.stalled import StalledDismissal


STALLED_DAYS = 10

TERMINAL_STAGES = [
    "Hired",
    "Rejected"
]


def is_application_stalled(application):
    """
    Application is stalled when it has remained
    in the same active pipeline stage for more
    than 10 days.
    """

    if application.stage in TERMINAL_STAGES:
        return False

    if not application.stage_changed_at:
        return False

    cutoff = datetime.utcnow() - timedelta(
        days=STALLED_DAYS
    )

    return application.stage_changed_at < cutoff


def is_stall_dismissed(application):
    """
    A dismissal only applies to this exact
    occurrence of the current stage.
    """

    dismissal = (
        StalledDismissal.query
        .filter_by(
            application_id=application.id,
            stage=application.stage,
            stage_started_at=application.stage_changed_at
        )
        .first()
    )

    return dismissal is not None


def get_stalled_applications():
    """
    Return stalled applications whose current
    stall alert has not been dismissed.
    """

    cutoff = datetime.utcnow() - timedelta(
        days=STALLED_DAYS
    )

    candidates = (
        Application.query
        .filter(
            Application.stage.notin_(
                TERMINAL_STAGES
            ),
            Application.stage_changed_at < cutoff
        )
        .order_by(
            Application.stage_changed_at.asc()
        )
        .all()
    )

    visible = []

    for application in candidates:

        if not is_stall_dismissed(application):
            visible.append(application)

    return visible