from app import app
from extensions import db
from models.user import User


users = [
    {
        "name": "Demo Recruiter",
        "email": "recruiter@example.com",
        "password": "Recruiter@123",
        "role": "recruiter"
    },
    {
        "name": "Demo Recruiter 2",
        "email": "recruiter2@example.com",
        "password": "Recruiter2@123",
        "role": "recruiter"
    },
    {
        "name": "Demo Interviewer",
        "email": "interviewer@example.com",
        "password": "Interviewer@123",
        "role": "interviewer"
    },
    {
        "name": "Interviewer_1",
        "email": "interviewer1@example.com",
        "password": "Interviewer1@123",
        "role": "interviewer"
    },
    {
        "name": "Interviewer_2",
        "email": "interviewer2@example.com",
        "password": "Interviewer2@123",
        "role": "interviewer"
    },
    {
        "name": "Interviewer_3",
        "email": "interviewer3@example.com",
        "password": "Interviewer3@123",
        "role": "interviewer"
    }
]


with app.app_context():

    db.create_all()

    for user_data in users:

        existing_user = User.query.filter_by(
            email=user_data["email"]
        ).first()

        if existing_user:
            print(
                f"Already exists: "
                f"{existing_user.name} ({existing_user.email})"
            )
            continue

        user = User(
            name=user_data["name"],
            email=user_data["email"],
            role=user_data["role"]
        )

        user.set_password(user_data["password"])

        db.session.add(user)

        print(
            f"Created: "
            f"{user_data['name']} ({user_data['email']})"
        )

    db.session.commit()

    print("\nUser seeding completed successfully.")