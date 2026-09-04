

# AI Prompts

AI was used as a development productivity tool during the project. The overall
architecture, feature breakdown, database design, workflow rules, authorization
model, and implementation approach were decided by me.

I mainly used AI for repetitive coding assistance, debugging, explaining error
messages, checking edge cases, and making small UI/CSS improvements. Generated
suggestions were reviewed, adapted to the existing codebase, and tested locally
before being kept.


## 1. Basic folder structure

**Promt**
“I am sharing the 10 requirements/goals of my project. Based on these requirements, suggest a basic folder structure to start the project using Python, Flask, HTML, CSS, and JavaScript. Initially, I want to use SQLite as the database and later use PostgreSQL in production. Keep the structure simple and directly related to the requirements. Do not add unnecessary utility folders, extra abstractions, or advanced structures that I may not need at the beginning. If you have useful structural suggestions, mention them separately so I can decide whether to implement them.”

**what you got**
I got a basic folder structure containing app.py , templates, static, routes, models folders ,etc.

**What you corrected**
I added more folder like utility or some files in root directory as needed.

## 2. Debugging Flask / SQLAlchemy Errors

**Prompt**
“I am getting this SQLAlchemy/Flask error while running my application. Here is the traceback and the relevant code. Explain the cause and suggest the smallest change that fixes it without changing the existing project structure.”

**What you got**
An explanation of the likely source of the error and a suggested minimal code/configuration change to resolve it.

**What you corrected**
I identified the source of the error from the explanation, applied the appropriate change myself, and tested the application again to verify that the issue was resolved.

## 3. Database Schema 

**Prompt**
I am designing the database schema for my Hiring Pipeline project. I am sharing the project requirements/goals and the existing project context.

Based on these requirements, design a relational database schema for the application using SQLite initially, with the intention of moving to PostgreSQL in production. The schema should be designed in a way that the migration from SQLite to PostgreSQL does not require major changes to the application structure.

The application has two user roles: `recruiter` and `interviewer`. Recruiters manage job openings and applications, while interviewers can access applications assigned to them and submit interview feedback.

The hiring pipeline is:

Applied → Screening → Interview → Offer → Hired

An application can also be Rejected from any active stage and later reinstated to the exact stage from which it was rejected. The database should support this workflow without unnecessarily storing derived or duplicated information.

The project also requires job openings, candidate applications, interviewer assignments, interview scheduling, interviewer feedback, immutable application history/timeline, and stalled-application alerts with dismissal tracking.

The application needs server-side candidate search and filtering by candidate name/email, job, stage and source, sorting, pagination, bulk actions, CSV export, dashboard metrics, and pipeline reporting. Consider which columns should be indexed to support these operations efficiently.

Please identify the essential tables/entities and fields required for this Hiring Pipeline application. For each table, provide:

* table name;
* important columns and their data types;
* primary key;
* foreign keys;
* required vs optional fields;
* unique constraints;
* useful indexes;
* relationships with other tables.

Pay particular attention to the relationship between applications and interviewers. One application can have multiple interviewers, and one interviewer can be assigned to multiple applications, so use an appropriate relational design rather than assuming a single interviewer per application.

Also design the application history so that pipeline changes, rejection/reinstatement, feedback submission, and other important actions can be represented as an immutable timeline with information about the actor who performed the action.

For stalled applications, the design should support identifying when an application has remained in its current stage for more than ten days and whether the corresponding stalled alert has been dismissed.

Keep the schema normalized and practical for the current size of the project. Do not over-engineer it by adding unnecessary tables or features that are not part of the requirements. In particular, do not add tables for optional features such as candidate portals, resume parsing/skill matching, offer-letter generation, referral tracking, email notifications, or other features that are not currently being built.

Also explain which rules should be enforced by the database through constraints and which rules should remain in Flask/application code because they depend on business logic or the current pipeline state.

Finally, suggest the schema in a way that works cleanly with Flask-SQLAlchemy and keeps SQLite as the local development database while allowing PostgreSQL to be used later through the database connection configuration.

**What you got**
I got a relational database schema. 
**What you corrected**
I reviewed the suggested schema and made changes according to the actual relationships required by my project. For example, I adjusted the relationships between tables such as users, job_openings, applications, application_interviewers, interview_schedules, feedback, application_events, and stalled_dismissals instead of accepting the proposed relationships directly. I also changed some fields and foreign-key relationships where they did not match my intended workflow. For instance, I ensured that the relationship between applications and interviewers was handled through application_interviewers, allowing multiple interviewers to be assigned to an application. I similarly reviewed the relationships between job_openings and applications, applications and application_events, and applications and interview_schedules.


# 4. Python / Flask Coding Issues

**Prompt**
“Here is the existing code. I want to achieve that role based authentication on server side ,make only simple changes if anything you find wrong. What is the simplest way to implement this while keeping the current structure?”

**What you got**
A simple implementation approach or code suggestion for the specific behaviour.

**What you corrected**
I evaluated the suggestion, selected the useful approach, and integrated it into my existing code rather than relying on AI to determine the overall project design.

# 5. Pipeline Edge-Case Verification

**Prompt**
“Review this pipeline transition function and identify any edge cases that could allow an invalid transition or produce an incorrect state.”

**What you got**
A review of the transition logic and potential edge cases that could cause invalid state changes.

**What you corrected**
The pipeline design itself was based on the assignment requirements: Applied → Screening → Interview → Offer → Hired, with rejection and reinstatement. I used AI only as a second check and then manually tested advancing stages, skipping stages, rejecting applications from different active stages, advancing rejected applications, reinstating rejected applications, and advancing hired applications. Any required changes were then made and tested manually.

# 6. Sorting and Filtering Applications

**Prompt**
I am implementing sorting and filtering functionality in the Applications section of my Hiring Pipeline project.

The Applications page needs to support filtering and sorting based on multiple parameters, such as job opening, application stage, candidate name/email, source, and other relevant application fields. Sorting should allow the recruiter to change the order of the displayed applications based on appropriate fields, such as candidate name, application date, or current stage.

I already understand the required filtering and sorting behaviour and how it should work from the user's perspective.

Based on my existing Flask route, SQLAlchemy models, HTML/Jinja template, and JavaScript, show me how to implement the filtering and sorting while keeping the existing project structure.

Please make sure that:

multiple filters can work together;
sorting can be combined with filtering;
the selected filters and sorting option are preserved when the page is refreshed or paginated;
filtering is performed on the server side rather than loading all applications and filtering them only with JavaScript;
the implementation works with the existing pagination;
the same filtering logic can also be reused for CSV export;
no duplicate Applications page or separate filtering system is created;
existing functionality and UI are not unnecessarily changed.

Keep the solution straightforward and focused on the implementation details. Do not redesign the feature or introduce unnecessary abstractions. I mainly want help with the time-consuming coding, query construction, parameter handling, and edge cases while keeping the final implementation decisions under my control.

**What you got**
AI provided implementation guidance for combining multiple filters with SQLAlchemy queries and adding sorting parameters to the existing Applications route. It also showed how the selected filters and sort option could be preserved across pagination and reused when generating the CSV export.

**What you corrected**
I reviewed the suggested implementation and adapted it to my existing applications route, models, template, and project structure. I decided which filtering and sorting parameters were actually required and adjusted the query logic accordingly. I also verified that multiple filters could work together, sorting worked correctly with the filters, and pagination did not lose the selected parameters. Rather than using AI to decide the feature design, I used it mainly to reduce the time spent writing repetitive query and parameter-handling code, while I tested and corrected the final behaviour myself.

# 7. Export Csv 

**Prompt**
I want to add CSV export functionality to my Hiring Pipeline project.
My Applications page already has filtering functionality, such as filtering applications by job opening, pipeline stage, source, and other available criteria. I want to add an “Export CSV” option that exports **only the applications currently matching the selected filters**, rather than exporting every application in the database.

How can I implement this in my existing Flask, SQLAlchemy, HTML, CSS, and JavaScript project?

Please explain how to:
* reuse the existing application filtering logic for the CSV export;
* pass the currently selected filter values to the export route;
* query only the filtered applications from the database;
* generate the CSV file on the server using Python;
* include the appropriate application/candidate fields in the CSV;
* allow the recruiter to download the generated CSV file;
* ensure that exporting does not change or reset the current filters.

Please keep the implementation simple and consistent with my existing project structure. Do not create a separate filtering system just for CSV export, and do not change the existing Applications page functionality unnecessarily.

**What you got**
AI suggested creating a dedicated CSV export endpoint that receives the same filter parameters used by the Applications page. The endpoint could then apply those filters to the database query, generate a CSV containing the matching applications, and return it as a downloadable file.

**What you corrected**
I reused the existing application filtering logic instead of creating a second filtering system specifically for CSV export. I made the export functionality use the same selected filters from the Applications page, so the exported CSV contains only the applications currently matching the recruiter's filters. I also kept the export as an additional action on the existing Applications page rather than creating a separate export page or changing the existing filtering and pagination functionality.

# 8. CSS and Layout Debugging

**Prompt**
“The table is overflowing horizontally and the View button is being cut off. Here is the current HTML and CSS. Suggest CSS changes that keep the existing columns and functionality while fitting the available page width.”

**What you got**
An initial CSS solution intended to control the table width, column sizing, text overflow, and action-column layout.

**What you corrected**
The first suggestion did not completely solve the problem. I checked the rendered page myself, identified the remaining overflow, and adjusted the table layout, column widths, text overflow, and action-column sizing. I then retested the page until the complete View button was visible.

# 9. Jinja / HTML Formatting

**Promt**
I am working on the Jinja templates for my Flask-based Hiring Pipeline application. Several pages display dynamic data coming from the backend, including applications, pipeline stages, interview information, user roles, application history, and dashboard data.

I want to keep the existing HTML structure and UI design, but I need help implementing and organizing the Jinja template logic required to render this dynamic data correctly.

Based on the existing Flask routes, variables passed from the backend, and HTML templates, identify where Jinja expressions, conditional rendering, loops, and reusable template patterns should be used.

For example, the templates may need to:

display different information depending on the user's role;
conditionally show actions based on the current application stage;
render application history/events dynamically;
display interviewer and interview information;
show different buttons or statuses depending on application state;
handle optional or missing data without causing Jinja errors;
iterate through database records and display them consistently;
preserve the existing HTML and CSS structure.

Please provide the necessary Jinja changes while keeping the business logic in Flask/Python rather than unnecessarily moving it into the templates.

Do not redesign the pages or introduce unnecessary template abstractions. Focus on integrating the dynamic backend data correctly into the existing templates and maintaining consistency across related pages.

**What you got**
AI helped identify where Jinja loops, conditionals, variable expressions, and optional-value handling could be used to connect the backend data with the existing HTML templates. It also suggested ways to handle role-dependent actions, application states, history events, and dynamically generated records without duplicating large sections of HTML.

**What you corrected**
I reviewed the suggested Jinja implementation against my actual Flask routes and the variables being passed to each template. I corrected the template logic wherever it did not match my actual application state or backend data.

# 10.reusing the existing Applications page filtering instead of creating a separate page for each job

**Prompt**
I want to improve the application viewing flow in my Hiring Pipeline project.

Currently, I have a main Applications page that already supports filtering applications, including filtering by job opening. I do not want to create a separate page or separate route just to show applications belonging to a particular job opening.

I want the Job Openings page to use the existing Applications page and its filtering functionality. For example, when a recruiter clicks “View Applications” for a particular job opening, it should open the existing Applications page with that job already selected as a filter, so only applications for that job are displayed.

Please explain how I can implement this while reusing the existing route, template, filtering logic, and UI as much as possible.

I am using Flask with Jinja templates, SQLAlchemy, HTML, CSS, and JavaScript.

Please consider:

How to pass the selected job opening ID from the Job Openings page to the existing Applications route.
How the Applications route can read that value and apply it as the initial job filter.
How to preserve the existing filtering, searching, sorting, pagination, and bulk-action functionality.
How to avoid creating a duplicate “applications for this job” page or duplicate filtering logic.
How to keep the implementation simple and consistent with the existing project structure.
Do not redesign the existing Applications page or change unrelated functionality.

The goal is to follow the DRY principle by having one Applications page and one filtering implementation that can be used both for general application browsing and for viewing applications belonging to a specific job opening.

**What you got***
AI suggested reusing the existing Applications page instead of creating a separate page for applications belonging to each job opening. The approach was to pass the selected job_id from the Job Openings page to the existing Applications route and use it as the initial filter. This allowed the existing search, filtering, sorting, pagination, and bulk-action functionality to remain available.

**What you corrected**
I implemented the suggested approach within my existing project structure and modified the relationship between the Job Openings page and the Applications page. Instead of creating a new route or template such as job_applications.html, I made the View Applications action pass the relevant job_id to the existing Applications page. I then used that value to preselect the job filter and display only the applications associated with that job. This avoided duplicate pages and filtering logic while keeping the existing Applications functionality unchanged.

# 11. Apply same UI frontend on similar pages

**Prompt**
I am sharing an existing HTML template along with its corresponding CSS file. I am also sharing my `base.html` file and the other HTML pages of my Flask project.

Based on the existing HTML and CSS, generate the required CSS code for the other pages so that all pages follow the same visual design, spacing, typography, buttons, tables, forms, cards, colors, and overall layout style.

For pages that serve a similar purpose, reuse the same styling patterns instead of creating completely different designs. For example, the interviewer's Applications page, recruiter's Applications page, and Job Openings page should have a consistent application-management style.

I also want the `base.html` styling to provide a consistent common design across both the Interviewer Dashboard and Recruiter Dashboard, while still allowing each dashboard to have its own page-specific elements where necessary.

Please inspect the existing HTML structure and CSS carefully before generating the new CSS. Do not unnecessarily change the HTML structure, functionality, routes, Jinja logic, or existing features. Reuse existing CSS classes and patterns wherever possible, and only introduce new classes when they are actually required.
Keep the CSS clean, simple, and consistent with the existing design rather than introducing a completely new UI or framework.

The main goal is to make the entire application look like one coherent product, where related pages have the same visual language and common components behave consistently across the application.

**What you got**
Based on the htlm files i share , i got css code 

**What i correct**
I manually structure some table width , some buttons or headers styles


# 12. Deployment Configuration

**Prompt**
“My Flask application currently uses SQLite through SQLAlchemy and I want the database URL to come from an environment variable so the same application can use PostgreSQL in production. How can I do this while keeping SQLite as the local fallback?”

**What you got**
Guidance on environment-based database configuration, PostgreSQL driver requirements, and keeping the production database credentials outside the repository.

**What you corrected**
I kept the configuration deliberately simple: SQLite remains the local fallback, DATABASE_URL selects the production database, secrets remain outside the repository, and the required PostgreSQL dependency is added. I postponed the actual deployment until the application's functional verification was complete.


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