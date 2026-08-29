from extensions import db


class ApplicationInterviewer(db.Model):
    __tablename__ = "application_interviewers"

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id"),
        primary_key=True
    )

    interviewer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    )

    assigned_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    application_id = db.Column(
        db.Integer,
        db.ForeignKey("applications.id"),
        nullable=False
    )

    interviewer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )