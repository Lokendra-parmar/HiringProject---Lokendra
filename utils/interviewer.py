from models.interview import ApplicationInterviewer


def is_assigned_interviewer(application_id, user_id):

    assignment = (
        ApplicationInterviewer.query
        .filter_by(
            application_id=application_id,
            interviewer_id=user_id
        )
        .first()
    )

    return assignment is not None