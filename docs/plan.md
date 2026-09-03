# Plan

Answer each of these, in your own words.

- How did you break the work into sessions?
- What order did you build in, and why that order?
- What did you estimate versus what it actually took?
- What did you cut when you ran short?

# Plan

The project was built incrementally around the ten required behaviours rather than starting with visual polish. The exact time was not tracked minute-by-minute, so the figures below are approximate rather than fabricated precise measurements.

## Session breakdown

### Session 1 — Project setup and authentication

- Set up the Flask application structure.
- Added Flask-SQLAlchemy and Flask-Login.
- Created the user model and login flow.
- Added recruiter/interviewer role checks.
- Verified that an interviewer cannot use recruiter-only routes.

**Estimate:** about 1.5–2 hours  
**Actual:** roughly in this range.

### Session 2 — Jobs and applications

- Built job opening CRUD/status actions.
- Added archive/restore behaviour.
- Built application creation/editing.
- Linked applications to exactly one job.
- Added the job → application navigation.

**Estimate:** about 2 hours  
**Actual:** roughly 2 hours.

### Session 3 — Pipeline and interview panel

- Implemented Applied → Screening → Interview → Offer → Hired.
- Added rejection and exact-stage reinstatement.
- Added server-side validation against illegal stage jumps.
- Added interviewer assignment/removal.
- Added interviewer-specific application access.

**Estimate:** about 2 hours  
**Actual:** roughly 2–2.5 hours because workflow edge cases needed verification.

### Session 4 — Finding and acting on candidates

- Added server-side search.
- Added job/stage/source filters.
- Added sorting and pagination.
- Added bulk advance/reject with per-candidate results.
- Added CSV export.

**Estimate:** about 1.5–2 hours  
**Actual:** roughly 2 hours.

### Session 5 — Dashboard, interviews, history and stalled alerts

- Added dashboard metrics and charts.
- Added interview scheduling and interviewer feedback.
- Added immutable application events/timeline.
- Added stalled-application detection and dismissal.
- Improved the dashboard and candidate detail presentation.

**Estimate:** about 2 hours  
**Actual:** roughly 2–2.5 hours.

### Final verification / deployment preparation

- Added multiple demo users.
- Tested role boundaries and pipeline rules.
- Fixed application-list layout issues.
- Prepared `requirements.txt`.
- Kept SQLite as the working local database while making configuration ready for PostgreSQL.
- Started deployment preparation without deploying prematurely.

**Estimate:** about 1.5 hours  
**Actual:** the remaining time was used for verification and fixes.

## Why this order?

Authentication and roles were built first because every later feature has an authorization boundary. Jobs came before applications because every application must belong to a job. The pipeline was then implemented as a separate utility so that the same rules could be used by single and bulk actions. Interview assignment and feedback depended on applications already existing. Search, bulk actions and dashboards were built after the core data model and workflows were stable.

Visual refinement was intentionally kept after the required behaviour. This avoided spending the limited time polishing screens before the server-side rules were correct.

## Estimated versus actual

The original target was approximately twelve hours, as suggested by the assignment. I used that as a scope guide rather than trying to time every individual coding action. The work was close to the intended budget, but some tasks took longer than expected because they required manual verification of edge cases, especially pipeline transitions, interviewer authorization, bulk-action partial failures, history, and stalled alerts.

## What I cut when time became tight?

I did not spend time on the optional stretch features. In particular, I left out:

- public careers page;
- structured interview scorecards;
- candidate-facing portal;
- resume skill tagging/search;
- offer-letter generation;
- source-of-hire reporting;
- email digests;
- referral tracking;
- self-service interview scheduling links.

I also avoided introducing a separate frontend framework. The server-rendered Flask/Jinja approach was sufficient for the requirements and reduced deployment and maintenance overhead.
"""