from extensions import db
from models.event import ApplicationEvent


def create_application_event(
    application_id,
    event_type,
    actor_id=None,
    message=None,
    old_stage=None,
    new_stage=None
):
    event = ApplicationEvent(
        application_id=application_id,
        event_type=event_type,
        actor_id=actor_id,
        message=message,
        old_stage=old_stage,
        new_stage=new_stage
    )

    db.session.add(event)

    return event