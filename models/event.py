from extensions import db


class ApplicationEvent(db.Model):
    __tablename__ = "application_events"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id"),
        nullable=False
    )

    event_type = db.Column(
        db.String(50),
        nullable=False
    )

    old_stage = db.Column(
        db.String(30),
        nullable=True
    )

    new_stage = db.Column(
        db.String(30),
        nullable=True
    )

    actor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    message = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    application = db.relationship(
        "Application",
        back_populates="events"
    )