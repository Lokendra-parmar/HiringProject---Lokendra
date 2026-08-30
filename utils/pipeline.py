from datetime import datetime

from extensions import db
from models.event import ApplicationEvent


PIPELINE_STAGES = [
    "Applied",
    "Screening",
    "Interview",
    "Offer",
    "Hired"
]


def advance_application(application, actor_id):
    """
    Move an application exactly one stage forward.
    """

    if application.stage == "Rejected":
        raise ValueError(
            "A rejected application must be reinstated first."
        )

    if application.stage == "Hired":
        raise ValueError(
            "A hired application cannot be advanced further."
        )

    current_index = PIPELINE_STAGES.index(
        application.stage
    )

    if current_index >= len(PIPELINE_STAGES) - 1:
        raise ValueError(
            "Application is already at the final stage."
        )

    old_stage = application.stage

    new_stage = PIPELINE_STAGES[current_index + 1]

    application.stage = new_stage

    application.stage_changed_at = datetime.utcnow()

    event = ApplicationEvent(
        application_id=application.id,
        event_type="STAGE_CHANGED",
        actor_id=actor_id,
        old_stage=old_stage,
        new_stage=new_stage,
        message=f"Application moved from {old_stage} to {new_stage}."
    )

    db.session.add(event)


def reject_application(application, actor_id):
    """
    Reject an application from any active pipeline stage.
    """

    if application.stage == "Rejected":
        raise ValueError(
            "Application is already rejected."
        )

    if application.stage == "Hired":
        raise ValueError(
            "A hired candidate cannot be rejected."
        )

    old_stage = application.stage

    application.stage = "Rejected"

    application.stage_changed_at = datetime.utcnow()

    event = ApplicationEvent(
        application_id=application.id,
        event_type="REJECTED",
        actor_id=actor_id,
        old_stage=old_stage,
        new_stage="Rejected",
        message=f"Application rejected from {old_stage} stage."
    )

    db.session.add(event)


def reinstate_application(application, actor_id):
    """
    Reinstate a rejected application to the exact
    stage it occupied immediately before rejection.
    """

    if application.stage != "Rejected":
        raise ValueError(
            "Only rejected applications can be reinstated."
        )

    # Find the rejection event.
    rejection_event = (
        ApplicationEvent.query
        .filter_by(
            application_id=application.id,
            event_type="REJECTED"
        )
        .order_by(ApplicationEvent.created_at.desc())
        .first()
    )

    if not rejection_event or not rejection_event.old_stage:
        raise ValueError(
            "Previous stage could not be determined."
        )

    previous_stage = rejection_event.old_stage

    old_stage = application.stage

    application.stage = previous_stage

    application.stage_changed_at = datetime.utcnow()

    event = ApplicationEvent(
        application_id=application.id,
        event_type="REINSTATED",
        actor_id=actor_id,
        old_stage=old_stage,
        new_stage=previous_stage,
        message=(
            f"Application reinstated to {previous_stage} stage."
        )
    )

    db.session.add(event)