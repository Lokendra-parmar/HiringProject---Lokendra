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

    application = db.relationship(
        "Application",
        backref=db.backref(
            "interviewer_assignments",
            lazy=True
        )
    )

    interviewer = db.relationship(
        "User",
        backref=db.backref(
            "application_assignments",
            lazy=True
        )
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

    application = db.relationship(
        "Application",
        backref=db.backref(
            "feedback_entries",
            lazy=True
        )
    )

    interviewer = db.relationship(
        "User",
        backref=db.backref(
            "feedback_entries",
            lazy=True
        )
    )

class InterviewSchedule(db.Model):
    __tablename__ = "interview_schedules"

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

    scheduled_at = db.Column(
        db.DateTime,
        nullable=False,
        index=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    application = db.relationship(
        "Application",
        backref=db.backref(
            "scheduled_interviews",
            lazy=True
        )
    )