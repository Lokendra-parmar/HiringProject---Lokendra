from extensions import db
from models.event import ApplicationEvent


def create_application_event(
    application,
    event_type,
    actor_id=None,
    old_stage=None,
    new_stage=None,
    message=None
):
    event = ApplicationEvent(
        application_id=application.id,
        event_type=event_type,
        actor_id=actor_id,
        old_stage=old_stage,
        new_stage=new_stage,
        message=message
    )

    db.session.add(event)

    return event