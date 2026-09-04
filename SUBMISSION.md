# Submission

## Links

- **GitHub repository:** https://github.com/Lokendra-parmar/HiringProject---Lokendra

- **Live application:** https://hiringproject-lokendra.onrender.com

## Notes for the reviewer

The application is deployed on Render and uses PostgreSQL in production.
our host sleeps when idle and the first request can take up to a minute, if page sh.

The application is a server-rendered Flask application. Please use the demo credentials below to explore the recruiter and interviewer workflows.

The interviewer account has intentionally limited access. Recruiter-only operations are protected on the server, so changing URLs or submitting requests directly does not bypass the role restrictions.

## Demo credentials

| Role | Email | Password |
|------|-------|----------|
| Recruiter | recruiter@example.com | Recruiter@123 |
| Recruiter | recruiter2@example.com | Recruiter2@123 |
| Interviewer | interviewer@example.com | Interviewer@123 |
| Interviewer | interviewer1@example.com | Interviewer1@123 |
| Interviewer | interviewer2@example.com | Interviewer2@123 |
| Interviewer | interviewer3@example.com | Interviewer3@123 |


## Stack

| Layer | What you used | Why |
|-------|---------------|-----|
| Frontend | HTML, CSS, Jinja2, JavaScript, Chart.js | Server-rendered UI keeps the application simple while providing the required dashboards and interactions. |
| Backend | Flask, Flask-Login, Flask-SQLAlchemy | Provides routing, authentication, authorization, business logic, and database access in a modular structure. |
| Database | SQLite locally, PostgreSQL in production | SQLite keeps local development simple, while PostgreSQL provides the production database. |
| Hosting | Render + Gunicorn | Provides a simple production deployment for the Flask application and PostgreSQL database. |

## Goal checklist

| # | Goal | Status | Notes |
|---|------|--------|-------|
| 1 | Recruiter and interviewer roles with server-side access control | Done | Recruiter and interviewer roles are implemented. Recruiter-only operations and interviewer application access are enforced server-side. |
| 2 | Job opening management | Done | Jobs support creation, editing, open/close status, archive/restore, with applications retained when a job is archived. |
| 3 | Application management | Done | Applications belong to one job and support candidate information, notes, editing, and job-based application viewing. |
| 4 | Hiring pipeline and rejection/reinstatement | Done | Applications move one stage at a time through Applied → Screening → Interview → Offer → Hired. Rejection and exact-stage reinstatement are supported. |
| 5 | Interviewer assignments and access | Done | Multiple interviewers can be assigned to applications, and interviewers can access their assigned applications and provide feedback. |
| 6 | Search, filters, sorting and pagination | Done | Server-side candidate search, job/stage/source filters, sorting, pagination, and total result counts are implemented. |
| 7 | Bulk actions and CSV export | Done | Bulk advance/reject actions provide individual success/failure results, and open applications can be exported as a CSV snapshot. |
| 8 | Dashboard and reporting | Done | Dashboard includes open positions, active applications, interviews this week, hires this month, job/stage breakdowns, and weekly application trends. |
| 9 | Immutable application history | Done | Application events record important actions including creation, stage changes, rejection/reinstatement, and feedback-related activity. |
| 10 | Stalled application alerts | Done | Applications remaining in the same stage for more than 10 days are flagged. Recruiters can dismiss alerts, and advancing to a new stage can produce a new alert later. |

## How much time did you actually spend?

Approximately **14 hours**, including implementation, debugging, testing, frontend refinement, PostgreSQL migration/deployment, and final verification.

The time was not tracked minute-by-minute, so the figure is an approximate total rather than a precise measurement.

## What would you do next, with another 12 hours?

With another 12 hours, I would focus primarily on improving the existing system rather than adding a large number of new features. I would strengthen automated testing around authorization and pipeline edge cases, improve validation and error handling, optimize frequently used database queries, add more detailed dashboard/reporting capabilities, and further refine the UI based on usability testing. I would also improve deployment and production observability so that application errors and performance issues are easier to diagnose.

## What are you least happy with in this codebase, and why?

The area I am least satisfied with is the level of automated test coverage. The important workflows and edge cases were manually verified, but the project would benefit from a more comprehensive automated test suite covering role permissions, pipeline transitions, rejection/reinstatement, interviewer access, bulk operations, and stalled-alert behaviour.

I would improve this by adding focused unit and integration tests around the business rules and route-level authorization. This would make future changes safer and reduce the need for repeated manual verification.