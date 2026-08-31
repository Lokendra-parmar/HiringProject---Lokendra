from extensions import db


class StalledDismissal(db.Model):
    __tablename__ = "stalled_dismissals"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id"),
        nullable=False,
        index=True
    )

    stage = db.Column(
        db.String(30),
        nullable=False
    )

    stage_started_at = db.Column(
        db.DateTime,
        nullable=False
    )

    dismissed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    dismissed_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )