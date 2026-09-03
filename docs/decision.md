# Decisions

## Decision 1 — Use Flask with server-rendered Jinja templates

- **Chose:** Flask + Jinja2 templates with small JavaScript enhancements.
- **Rejected:** Building a separate React/Vue frontend and REST API.
- **Why:** The assignment rewards working behaviour and judgement within a limited time. Server-rendered pages reduced the amount of frontend state, API plumbing and deployment configuration while still supporting the required UI.
- **Later reversed:** The first implementation of some candidate/application screens was deliberately simple. After the required functionality was stable, I revised the candidate detail and dashboard presentation to a more polished layout without changing the underlying architecture.

## Decision 2 — Keep pipeline rules in a dedicated utility

- **Chose:** Put stage-transition rules in `utils/pipeline.py`.
- **Rejected:** Duplicating the transition logic in each Flask route.
- **Why:** Single and bulk actions need identical rules. A shared function prevents the UI or one route from accidentally allowing a different transition.

## Decision 3 — Store the current stage on `applications`

- **Chose:** Store `stage` and `stage_changed_at` directly on the application.
- **Rejected:** Reconstructing the current stage and stall time from the event history on every request.
- **Why:** Current stage is read frequently by lists, dashboards and candidate pages. Direct storage keeps those queries simple and fast. Events remain the authoritative history of how the application got there.

## Decision 4 — Use an event table for immutable history

- **Chose:** Append application events to `application_events`.
- **Rejected:** Maintaining a single mutable “last action” field or overwriting history.
- **Why:** The requirement explicitly asks for history that cannot be rewritten. Separate events preserve old/new stages, actor and event details over time.

## Decision 5 — Model interviewer assignment as a many-to-many relationship

- **Chose:** `application_interviewers` as a join table between applications and users.
- **Rejected:** A single `interviewer_id` column on applications.
- **Why:** The requirement allows any number of interviewers per application and any interviewer to work on many applications. A join table matches that relationship directly.

## Decision 6 — Enforce authorization on the server

- **Chose:** Use role decorators plus explicit interviewer-assignment checks.
- **Rejected:** Only hiding buttons in Jinja templates.
- **Why:** Hiding a button is not security. A user can still send a request manually. The route must independently verify the user's role and, for interviewers, their assignment to the application.

## Decision 7 — Keep SQLite locally and make PostgreSQL environment-driven

- **Chose:** SQLite fallback for local development and `DATABASE_URL` for PostgreSQL.
- **Rejected:** Hard-coding PostgreSQL credentials or changing the whole local workflow immediately.
- **Why:** SQLite makes local development simple, while the environment-variable configuration allows the same application to use managed PostgreSQL in production. It also lets deployment preparation happen without risking the working local database.

## Decision 8 — Treat feedback as both data and timeline history

- **Chose:** Keep feedback in the `feedback` table and create an immutable feedback-submission event.
- **Rejected:** Showing feedback only in a separate feedback section.
- **Why:** The assignment explicitly says feedback is part of the application timeline. The separate table supports structured retrieval, while the event makes the submission part of the immutable audit trail.
