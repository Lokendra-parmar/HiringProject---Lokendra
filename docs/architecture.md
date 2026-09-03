# Architecture

Answer each of these, in your own words, once the system has taken real shape.

- What are the moving pieces, and how do they talk to each other?
- Where does each piece run?
- What is the request path for one representative user action, end to end?
- What did you decide *not* to build, and why?

## Overview

Hiring Pipeline is a server-rendered Flask application for recruiters and interviewers. The application uses Flask for HTTP routing and request handling, Flask-Login for authentication/session management, Flask-SQLAlchemy for database access, Jinja2 templates for server-side HTML rendering, and small utility modules for pipeline rules, role checks, interviewer access, timezone conversion, and stalled-application logic.

The current local environment uses SQLite. The application is intentionally configured so that the database connection can be supplied through the `DATABASE_URL` environment variable, allowing the same application code to use PostgreSQL in production.

## Moving pieces

- **Flask application (`app.py`)**: creates the application, initializes extensions, registers blueprints, and registers the Flask-Login user loader.
- **Configuration (`config.py`)**: loads environment variables and selects the database URL. It falls back to local SQLite when `DATABASE_URL` is not set.
- **Extensions (`extensions.py`)**: owns the shared `SQLAlchemy` and `LoginManager` instances.
- **Routes / blueprints**:
  - `routes/auth.py`: login, logout, and the root redirect.
  - `routes/dashboard.py`: recruiter/interviewer dashboard and dashboard metrics.
  - `routes/jobs.py`: job opening management.
  - `routes/applications.py`: application creation/editing, search/filter/sort/pagination, pipeline actions, bulk actions, CSV export, and stalled-alert dismissal.
  - `routes/interviews.py`: interviewer assignment/removal, interviewer application list, feedback, and interview scheduling.
- **Models**: represent users, jobs, applications, interviewer assignments, feedback, interviews, immutable application events, and stalled-alert dismissals.
- **Utilities**:
  - pipeline utilities enforce legal stage transitions;
  - role decorators enforce server-side role access;
  - interviewer utilities verify assignment;
  - stalled utilities determine whether an application has remained in its current stage for more than ten days;
  - application-event helpers create timeline records;
  - timezone utilities format timestamps for the UI.
- **Jinja templates and CSS**: render the server response and provide the browser UI. Search, filtering, sorting, pagination, authorization and business rules remain server-side.
- **Chart.js**: used by the dashboard for browser-side chart rendering after the server supplies the aggregated data.
- **Database**: SQLite locally and PostgreSQL for the planned production environment.

## Where each piece runs

During local development, Flask, the templates, Python business logic, and SQLite database run on the developer's machine.

For production, the planned architecture is a Render web service running the Flask application with Gunicorn, connected to a managed Render PostgreSQL database. Secrets and connection strings will be supplied as environment variables rather than committed to the repository.

The browser only receives rendered HTML, CSS, JavaScript and chart data. It does not contain the authoritative hiring-pipeline rules.

## Representative request: advancing an application

1. A recruiter logs in through `/login`. Flask-Login creates the authenticated session.
2. The recruiter opens a candidate detail page.
3. The recruiter submits the **Advance Stage** form. The browser sends a POST request to `/applications/<application_id>/advance`.
4. The route is protected by the recruiter-only role decorator.
5. The route loads the application from the database and calls `advance_application()` in `utils/pipeline.py`.
6. The pipeline utility checks the current stage. It refuses rejected/hired applications and only permits the immediate next stage.
7. On a valid move, the application's stage and stage-change timestamp are updated and an immutable `STAGE_CHANGED` event containing the old stage, new stage and actor is added.
8. The transaction is committed.
9. Flask redirects back to the candidate detail page.
10. The page reloads the application and its event history from the database, so the new stage and timeline event are visible.

This separation means a user cannot bypass the pipeline rules simply by manually constructing an HTTP request.

## Security boundary

The UI hides controls that a role should not use, but authorization is also enforced on the server. Recruiter-only routes use the role decorator. Interviewer candidate access is additionally checked against the interviewer/application assignment before the detail page is shown. Interviewers therefore cannot obtain another application's pipeline merely by changing an ID in the URL.

## Deliberately not built

The assignment's ten required goals were prioritized over optional stretch work. I did not build a public careers page, structured scorecards, self-service scheduling links, a candidate-facing portal, resume skill search/tagging, offer-letter generation, source-of-hire reporting, email digests, or referral tracking.

I also kept the application server-rendered instead of introducing a separate frontend SPA. That reduced deployment complexity and kept the limited development time focused on authorization, pipeline correctness, immutable history, search, bulk actions, dashboard reporting, and stalled alerts.
