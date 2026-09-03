# AI prompts

AI was used as a development assistant for implementation, debugging, UI refinement, documentation and deployment preparation. I reviewed and tested the generated suggestions rather than treating them as authoritative.

The prompts below are representative of the actual sequence of work.

## 1. Project setup and debugging

### Prompt

“Tell me how to structure this Flask hiring pipeline project and implement the required recruiter/interviewer roles with server-side authorization.”

### What I got

Suggestions for Flask blueprints, Flask-Login authentication, role decorators and separate route modules.

### What I corrected

I kept the structure compatible with the existing project instead of blindly introducing a new architecture. I also tested recruiter-only and interviewer-only access manually.

## 2. Database and Flask issues

### Prompt

“I am getting this Flask/SQLAlchemy database error. Explain what it means and how to fix it without changing the assignment constraints.”

### What I got

Debugging suggestions around SQLAlchemy initialization, application context and table creation.

### What I corrected

I applied only the changes that matched the existing application-factory structure and assignment constraints. I did not add prohibited database seeding/table-creation behaviour to normal application startup.

## 3. Pipeline implementation

### Prompt

“Implement the hiring pipeline Applied → Screening → Interview → Offer → Hired. Allow rejection from any active stage and reinstatement to the exact stage rejected from. Reject illegal forward skips on the server.”

### What I got

A pipeline utility with functions for advance, reject and reinstate.

### What I corrected

I verified the rules manually, including rejecting from different stages, reinstating to the previous stage, attempting to advance a rejected application, attempting to advance a hired application, and ensuring only the next stage can be reached.

## 4. Search, filtering and bulk actions

### Prompt

“Implement server-side candidate search by name/email, job/stage/source filters, sorting, pagination, bulk advance/reject with per-candidate success or failure, and CSV export.”

### What I got

Route/query logic using SQLAlchemy filters, pagination and per-application bulk processing.

### What I corrected

I checked that filtering and search happen in the database query rather than in browser JavaScript, and verified that one invalid application in a bulk action does not hide the result for the other selected applications.

## 5. Dashboard and UI refinement

### Prompt

“Improve the Hiring Pipeline dashboard UI and make it look modern while keeping the existing Flask/Jinja functionality.”

### What I got

A more polished dashboard with metric cards, charts, pipeline breakdown and stalled-application area.

### What I corrected

I kept the underlying routes/data intact and verified that the dashboard still showed the required metrics. I also chose not to redesign the candidate detail page after its required functionality and layout were already working well.

## 6. Wrong UI output: applications table

### Prompt

“Make the applications table fit the page without horizontal scrolling while keeping all columns and the View button usable.”

### What I got

An initial CSS adjustment that reduced some spacing but still allowed the table/button area to overflow and cut off the View button.

### What I corrected

I inspected the rendered result instead of assuming the CSS was correct. I changed the table to use the available width with fixed column proportions, controlled overflow, text ellipsis and tighter action-column sizing. I retested the page until the table and View button were usable.

## 7. Application history and feedback

### Prompt

“The application timeline must show actor information and interviewer feedback must be part of the immutable timeline. How should I model and display that?”

### What I got

A suggestion to relate events to the user who performed them and create a timeline event when feedback is submitted.

### What I corrected

I kept the separate feedback record for structured feedback and made the feedback submission create an application event as well. I also checked the timeline template so event messages and actors can be displayed without allowing event editing/deletion.

## 8. Multiple demo users

### Prompt

“Create safe seed data for multiple recruiter and interviewer accounts, avoid duplicate emails, and hash passwords using the existing User model.”

### What I got

A seed script that checks whether each email already exists before creating a user and uses the model's password hashing method.

### What I corrected

I retained the existing password-hashing implementation and tested the resulting accounts by logging in with both roles and checking their permissions.

## 9. Deployment preparation

### Prompt

“My Flask project currently uses SQLite. How should I prepare it for PostgreSQL and Render while keeping SQLite working locally?”

### What I got

An environment-driven `DATABASE_URL` configuration, PostgreSQL driver dependency and a production server dependency.

### What I corrected

I kept SQLite as the fallback so local development continued to work. I added the required packages to `requirements.txt` and prepared the configuration for PostgreSQL without deploying until the application's functionality was completely verified.

## Overall AI verification approach

AI-generated code was treated as a starting point. For each important feature I inspected the code, integrated it into the existing project structure, ran the Flask application, exercised the relevant UI, and fixed behaviour that did not match the assignment. The table-layout issue above is an example where the first generated change was not accepted simply because it looked reasonable in code.










# Improved

# AI Prompts

AI was used as a development productivity tool during the project. The overall
architecture, feature breakdown, database design, workflow rules, authorization
model, and implementation approach were decided by me.

I mainly used AI for repetitive coding assistance, debugging, explaining error
messages, checking edge cases, and making small UI/CSS improvements. Generated
suggestions were reviewed, adapted to the existing codebase, and tested locally
before being kept.

## 1. Debugging Flask / SQLAlchemy errors

### Purpose
Debugging errors encountered while running the application.

### Prompt
"I am getting this SQLAlchemy/Flask error while running my application.
Here is the traceback and the relevant code. Explain the cause and suggest
the smallest change that fixes it without changing the existing project
structure."

### How I used the response
I used the explanation to identify the source of the error and then applied
the appropriate change myself. I tested the application again after the fix.

---

## 2. Small C++ / Python / Flask coding issues

### Purpose
Saving time on small implementation details while working on the project.

### Prompt
"Here is the existing code. I want to achieve [specific small behaviour].
What is the simplest way to implement this while keeping the current
structure?"

### How I used the response
AI was used for small pieces of implementation rather than deciding the
overall design. I selected the useful approach and integrated it into my
existing code.

---

## 3. Pipeline edge-case verification

### Purpose
Checking whether the implemented pipeline rules covered unusual cases.

### Prompt
"Review this pipeline transition function and identify any edge cases that
could allow an invalid transition or produce an incorrect state."

### How I used the response
The pipeline design itself was based on the assignment requirements:
Applied → Screening → Interview → Offer → Hired, with rejection and
reinstatement. AI was used as a second check for edge cases.

I then manually tested cases such as:
- advancing one stage;
- attempting to skip a stage;
- rejecting from different active stages;
- attempting to advance a rejected application;
- reinstating to the previous rejected stage;
- attempting to advance a hired application.

---

## 4. CSS and layout debugging

### Purpose
Fixing visual issues after checking the application in the browser.

### Prompt
"The table is overflowing horizontally and the View button is being cut off.
Here is the current HTML and CSS. Suggest CSS changes that keep the existing
columns and functionality while fitting the available page width."

### What happened
The first CSS suggestion did not completely solve the problem. The table still
overflowed and the action button was partially cut off.

### What I did
I checked the rendered page, identified the remaining overflow, and adjusted
the table layout, column widths, text overflow and action-column sizing.
I retested the page until the complete View button was visible.

This was a useful example of AI being an iterative debugging tool rather than
a replacement for testing.

---

## 5. Jinja / HTML formatting

### Purpose
Making small presentation changes in existing templates.

### Prompt
"I have this Jinja/HTML element. I don't want the text to appear bold.
What is the simplest HTML/CSS change?"

### How I used the response
I used the suggestion directly for a small presentation change and kept the
existing template structure.

---

## 6. Deployment configuration

### Purpose
Understanding the changes required to move from local SQLite development to
PostgreSQL deployment.

### Prompt
"My Flask application currently uses SQLite through SQLAlchemy and I want
the database URL to come from an environment variable so the same application
can use PostgreSQL in production. How can I do this while keeping SQLite as
the local fallback?"

### How I used the response
The project already used environment-based configuration. I used AI to check
the deployment implications and PostgreSQL driver requirements, then kept the
configuration deliberately simple:

- SQLite remains the local fallback.
- `DATABASE_URL` selects the production database.
- Secrets are kept outside the repository.
- PostgreSQL support is added through the appropriate Python dependency.

Deployment itself was intentionally postponed until functional verification
was complete.

---

## 7. Documentation review

### Purpose
Checking that the required take-home documentation answered the questions
asked by the assignment.

### Prompt
"Review this architecture/schema/decision document against the assignment
requirements and identify any missing topics."

### How I used the response
I used AI as a checklist/review tool. The actual project architecture,
database relationships, trade-offs and development decisions were based on
my implementation and the requirements.

---

## How AI was used overall

AI was not used to determine the core architecture of the application or to
replace implementation/testing.

The main engineering decisions were made first and then implemented in the
project. AI was most useful for:

- debugging error messages;
- checking small pieces of syntax or implementation;
- repetitive coding tasks;
- identifying edge cases;
- CSS/layout troubleshooting;
- explaining unfamiliar framework behaviour;
- reviewing documentation for completeness.

For generated suggestions, I followed a simple process:

1. Identify the problem myself.
2. Ask AI for a focused suggestion.
3. Compare the suggestion with the existing architecture.
4. Modify it where necessary.
5. Run the application and test the behaviour.
6. Keep it only if it actually solved the problem.

The final code therefore reflects the project's requirements and my design
choices rather than being copied wholesale from AI output.