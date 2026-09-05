# Hiring Pipeline

A web-based Hiring Pipeline application built with Flask that helps recruiters and interviewers manage job openings, candidate applications, hiring stages, interviews, feedback, and application history from a centralized interface.

The project focuses on providing a structured hiring workflow with role-based access, application tracking, filtering, sorting, pagination, CSV export, interview management, and pipeline reporting.


**LIVE link :**  https://hiringproject-lokendra.onrender.com/
---

## Features

### 1. Role-Based Access

The application supports two main user roles:

- **Recruiter**
  - Manage job openings
  - View and manage candidate applications
  - Advance applications through hiring stages
  - Reject and reinstate applications
  - Assign interviewers
  - Schedule interviews
  - View interviewer feedback
  - View application history
  - Export filtered applications to CSV
  - View hiring pipeline metrics and reports

- **Interviewer**
  - View applications assigned to them
  - View relevant candidate and job information
  - View scheduled interviews
  - Submit interview feedback
  - Access application information required for the interview process

---

## Hiring Pipeline

The application follows the required hiring workflow:

```text
Applied
   ↓
Screening
   ↓
Interview
   ↓
Offer
   ↓
Hired
```

An application can also be rejected from an active stage and later reinstated to the exact stage from which it was rejected.

```text
Active Stage
     ↓
  Rejected
     ↓
Reinstated
     ↓
Previous Rejected Stage
```

Applications cannot arbitrarily skip stages, and terminal states are handled according to the application rules.

---

## Application Management

The Applications section provides functionality for managing and reviewing candidate applications.

Features include:

- Candidate search
- Filtering by multiple parameters
- Filtering by job opening
- Filtering by application stage
- Filtering by source
- Sorting
- Pagination
- Bulk actions
- CSV export
- Application status management
- Application history/timeline

The existing Applications page is reused when viewing applications for a particular job opening.

Instead of creating a separate page for every job, the selected job is passed as a filter to the existing Applications page. This avoids duplicate routes, templates, and filtering logic.

---

## Search, Filtering and Sorting

Applications can be searched, filtered, and sorted using multiple parameters.

The filtering and sorting functionality is implemented on the server side using Flask and SQLAlchemy.

Multiple filters can be combined, and the selected filters and sorting options are preserved while navigating through paginated results.

The same filtering logic is also reused for CSV export so that the exported file contains the applications matching the currently selected filters.

---

## CSV Export

Recruiters can export applications to a CSV file.

The export functionality:

- Uses the existing application filtering logic
- Exports only applications matching the selected filters
- Supports the currently selected application criteria
- Generates the CSV on the server
- Allows the recruiter to download the filtered results
- Does not require a separate export page

This avoids maintaining a separate filtering implementation only for CSV generation.

---

## Interview Management

The application supports interview-related workflows including:

- Assigning interviewers to applications
- Supporting multiple interviewers for an application
- Scheduling interviews
- Viewing interview information
- Recording interviewer feedback

Interviewers can access applications assigned to them and submit their feedback through their dashboard.

---

## Application History

Important application actions are recorded as an application timeline/history.

This provides visibility into changes such as:

- Application creation
- Pipeline stage changes
- Rejection
- Reinstatement
- Interview-related actions
- Feedback-related actions
- Other important application events

The history provides an audit trail showing what happened to an application throughout the hiring process.

---

## Stalled Applications

The application identifies applications that remain in the same pipeline stage for more than the configured threshold.

For the current project requirements, applications that remain in a stage for more than **10 days** can be identified as stalled.

Recruiters can review these applications and manage the corresponding stalled alerts.

---

## Dashboard

The application provides separate dashboards for recruiters and interviewers.

### Recruiter Dashboard

The recruiter dashboard provides an overview of the hiring pipeline, including relevant application and job-opening information.

### Interviewer Dashboard

The interviewer dashboard focuses on applications and interviews assigned to the interviewer.

Both dashboards use the common application layout and styling provided through the base template while maintaining role-specific content.

---

## Technology Stack

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Jinja2

### Frontend

- HTML
- CSS
- JavaScript

### Database

- **SQLite** for local development
- **PostgreSQL** for production

### Development and Deployment

- Git
- GitHub
- Environment variables for configuration and secrets

---


## Database Design

The database is implemented using SQLAlchemy models.

The main entities include:

- `users`
- `job_openings`
- `applications`
- `application_interviewers`
- `interview_schedules`
- `feedback`
- `application_events`
- `stalled_dismissals`

---

## Local Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd hiring-pipeline
```

### 2. Create a Virtual Environment

On Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file if required by the application.

For local development, SQLite can be used as the database.

Example:

```env
DATABASE_URL=sqlite:///database.sqlite3
SECRET_KEY=your-secret-key
```

Do not commit secrets or sensitive configuration values to GitHub.

### 5. Run the Application

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

---

## Production Database

The application is designed so that SQLite can be used during local development while PostgreSQL can be configured for production.

The production database URL is supplied through an environment variable rather than being hard-coded into the application.

Example:

```env
DATABASE_URL=<production-postgresql-database-url>
```

This allows the same application codebase to work with different database environments.

---


## Testing and Verification

The application was manually tested during development.

Important scenarios included:

- Advancing an application by one stage
- Preventing invalid stage skipping
- Rejecting applications from different active stages
- Preventing advancement of rejected applications
- Reinstating applications to their previous rejected stage
- Preventing advancement of hired applications
- Assigning interviewers
- Scheduling interviews
- Submitting interview feedback
- Searching and filtering applications
- Combining multiple filters
- Sorting filtered results
- Maintaining filters during pagination
- Exporting filtered applications to CSV
- Viewing applications for a specific job using the existing Applications page
- Checking role-specific dashboard behaviour
- Verifying responsive table and layout behaviour

---

## Future Improvements

Possible future improvements include:

- Automated test coverage
- More advanced reporting
- Improved notification mechanisms
- Additional candidate-management functionality
- Production monitoring and logging
- More comprehensive PostgreSQL deployment configuration

These features are outside the current core implementation.

---

## License

This project was developed as part of a Hiring Pipeline take-home project.

