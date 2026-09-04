
# Decisions

This document records the main technical and product decisions made during
the implementation. The goal was to choose technologies and approaches that
fit the requirements, could be implemented reliably within the available
time, and would remain straightforward to deploy and maintain.

## 1. Flask instead of Django

- **Chose:** Flask.
- **Rejected:** Django.
- **Why:** The application is relatively small and has a focused set of
  workflows. Flask gives direct control over routes, blueprints, authentication,
  database access and templates without requiring the larger Django framework
  structure.
- **Why it fit this project:** The project needed several independent route
  groups (authentication, jobs, applications, dashboard and interviews), which
  Flask blueprints handle cleanly. It also allowed me to keep the application
  structure lightweight.

---

## 2. SQLAlchemy instead of raw SQL

- **Chose:** Flask-SQLAlchemy / SQLAlchemy ORM.
- **Rejected:** Writing raw SQL queries throughout the application.
- **Why:** The application has several related entities such as jobs,
  applications, users, interviewers, feedback and events. SQLAlchemy provides
  relationships, query composition and database abstraction while keeping the
  Python code readable.
- **Additional benefit:** It makes the later SQLite → PostgreSQL transition
  much easier because most application queries do not depend on SQLite-specific
  SQL.

---

## 3. SQLite for local development

- **Chose:** SQLite during local development.
- **Rejected:** Installing and maintaining a local PostgreSQL server from the
  beginning.
- **Why:** The application needed a simple local setup and the assignment
  required a relatively small development database. SQLite has no separate
  database server and makes starting the project quick.

---

## 4. PostgreSQL for production

- **Chose:** PostgreSQL for the production database.
- **Rejected:** Keeping SQLite in production.
- **Why:** PostgreSQL is better suited to a multi-user production application,
  provides stronger concurrency characteristics, richer indexing/query
  capabilities and is a natural fit for a managed deployment on Render.
- **Migration approach:** The application reads `DATABASE_URL` from the
  environment. SQLite remains the local fallback while PostgreSQL can be
  supplied in production without changing the application code.
---

## 5. Jinja2 server-rendered templates instead of React/Vue

- **Chose:** Flask + Jinja2 server-rendered HTML.
- **Rejected:** React, Vue or another separate frontend framework.
- **Why:** Most pages in the application are forms, tables, detail pages and
  dashboards. They do not require the complex client-side state management of a
  single-page application.
- **Benefit:** Authentication, authorization, filtering, pagination and
  business rules remain straightforward server-side operations.

---

## 6. Flask-Login instead of implementing authentication manually

- **Chose:** Flask-Login.
- **Rejected:** Building session management and authentication state manually.
- **Why:** Authentication is security-sensitive infrastructure. Flask-Login
  provides the established session/login primitives while allowing the
  application's own role checks to remain explicit.
  Passwords are not stored as plaintext. The `User`
  model uses Werkzeug password hashing and verification.

---

## 7. Role-based authorization on the server instead of UI-only restrictions

- **Chose:** Server-side role checks.
- **Rejected:** Simply hiding recruiter/interviewer buttons in HTML.
- **Why:** UI restrictions are not security boundaries. A user can manually
  construct an HTTP request even when a button is hidden.
- **Implementation:** Recruiter-only routes are protected by role checks, and
  interviewer access to an application is additionally verified against the
  interviewer/application assignment.

---

## 8. Dedicated pipeline utility instead of putting transition logic in routes

- **Chose:** A dedicated `utils/pipeline.py`.
- **Rejected:** Duplicating pipeline logic in each Flask route.
- **Why:** The same rules are needed for normal actions and bulk actions.
  Centralising them makes the rules easier to reason about and reduces the
  possibility that one endpoint accidentally allows a different transition.

  Only the next stage can be reached, rejected
  applications must be reinstated first, reinstatement returns to the exact
  rejected-from stage, and hired applications cannot be advanced further.

---

## 9. Event table instead of storing only the latest application action

- **Chose:** An append-only `application_events` table.
- **Rejected:** A single mutable `last_action` or `last_updated_reason`
  column on the application.
- **Why:** The assignment requires immutable history. A separate event record
  preserves old stage, new stage, actor, event type and timestamp.
- **Result:** The candidate detail page can reconstruct a timeline without
  modifying previous events.

---

## 10. Many-to-many interviewer assignment instead of one interviewer per application

- **Chose:** A join table, `application_interviewers`.
- **Rejected:** Adding a single `interviewer_id` column to applications.
- **Why:** The requirement allows multiple interviewers on one application and
  one interviewer to work with many applications.
- **Result:** The database structure directly represents the required
  many-to-many relationship.

---

## 11. Store current stage directly on the application

- **Chose:** Store `stage` and `stage_changed_at` on `applications`.
- **Rejected:** Calculating the current stage from the complete event history
  every time.
- **Why:** Current stage is one of the most frequently displayed and filtered
  pieces of application data. Storing it directly keeps normal queries simple.

---

## 12. Server-side search, filtering and pagination instead of loading everything

- **Chose:** SQLAlchemy queries with server-side search, filters, sorting and
  pagination.
- **Rejected:** Loading all applications into the browser and filtering them
  with JavaScript.
- **Why:** Server-side querying scales better and ensures that the visible
  result set and pagination totals are based on the database rather than the
  browser.
  Additional benefit: The same query approach can later benefit from
  PostgreSQL indexes and database-specific search features.

---

## 13. Chart.js instead of building dashboard charts manually

- **Chose:** Chart.js for dashboard visualisations.
- **Rejected:** Drawing charts manually with SVG/canvas code.
- **Why:** The dashboard only needs a small number of standard charts.
  Chart.js provides those visualisations without requiring a larger frontend
  framework.

---

## 14. A design decision that was later reversed

- **Initial choice:** Keep the application screens visually minimal while
  implementing the required backend behaviour.
- **Later change:** After the core functionality was stable, I revisited the
  dashboard and candidate/interview presentation and improved the visual
  hierarchy, cards, timeline presentation and dashboard charts.
- **Why** The minimal UI was useful during rapid functional
  development, but the final submission needed a clearer and more polished
  user experience.
  What I did not reverse: I kept the underlying Flask/Jinja architecture
  and server-side business rules. The visual refinement was deliberately
  separated from the core application design.

## 15. Gunicorn for the production Flask server

- **Chose:** Gunicorn for the planned production deployment.
- **Rejected:** Using Flask's built-in development server in production.
- **Why:** Flask's development server is intended for development and
  debugging. Gunicorn provides a proper WSGI application server for the
  production web service.
  Result: Render can run the Flask application through a production
  server command rather than relying on `app.run()`.

---

## 16. Environment variables for deployment configuration

- **Chose:** Environment variables for secrets and database configuration.
- **Rejected:** Hard-coding credentials or production database URLs in Python.
- **Why:** Secrets should not be committed to source control. The same code
  should also be usable in local and production environments.

---

## 17. Rejected the idea of deploying before functional verification

- **Chose:** Complete functional verification before deployment.
- **Rejected:** Deploying early and debugging primarily on the production
  service.
- **Why:** The application contains several security and workflow requirements
  where local testing is faster and safer. Deployment should be the final
  environment change rather than another source of debugging noise.
  Result: PostgreSQL/Render preparation is being done after the core
  application behaviour has been tested.

---



---

