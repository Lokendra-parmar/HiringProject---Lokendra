from app import app
from extensions import db
from models.user import User


with app.app_context():

    db.create_all()

    recruiter = User.query.filter_by(
        email="recruiter@example.com"
    ).first()

    if not recruiter:

        recruiter = User(
            name="Demo Recruiter",
            email="recruiter@example.com",
            role="recruiter"
        )

        recruiter.set_password("Recruiter@123")

        db.session.add(recruiter)


    interviewer = User.query.filter_by(
        email="interviewer@example.com"
    ).first()

    if not interviewer:

        interviewer = User(
            name="Demo Interviewer",
            email="interviewer@example.com",
            role="interviewer"
        )

        interviewer.set_password("Interviewer@123")

        db.session.add(interviewer)


    db.session.commit()

    print("Demo users created successfully.")