from extensions import db


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    job_opening_id = db.Column(
        db.Integer,
        db.ForeignKey("job_openings.id"),
        nullable=False,
        index=True
    )

    candidate_name = db.Column(
        db.String(150),
        nullable=False
    )

    candidate_email = db.Column(
        db.String(150),
        nullable=False,
        index=True
    )

    source = db.Column(
        db.String(100),
        nullable=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    stage = db.Column(
        db.String(30),
        nullable=False,
        default="Applied",
        index=True
    )

    applied_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    stage_changed_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    job = db.relationship(
        "JobOpening",
        back_populates="applications"
    )

    events = db.relationship(
        "ApplicationEvent",
        back_populates="application",
        lazy=True,
        order_by="ApplicationEvent.created_at"
    )