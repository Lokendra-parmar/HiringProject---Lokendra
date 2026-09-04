# Schema

Answer each of these, in your own words.

- Table by table: what columns and types does each one have?
- Which relationships are one-to-many, and which are many-to-many?
- Which constraints are enforced by the database, and which by application code — and why did you draw the line there?
- What did you deliberately denormalise?
- What would break first if this had 100x the data?

# Schema

The application uses SQLAlchemy models. SQLite is used for local development, while PostgreSQL is used in the deployed production environment. The schema is relational and keeps the main entities separate while using join/event tables where the relationship or history requires it.

## 1. `users`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `name` | String(100) | Required |
| `email` | String(150) | Required, unique, indexed |
| `password_hash` | String(255) | Required; stores a Werkzeug password hash, not plaintext |
| `role` | String(20) | Required; application supports `recruiter` and `interviewer` |
| `created_at` | DateTime | Database-generated creation timestamp |

A user can have many related application-event records as the actor and can participate in many application/interviewer assignments.

## 2. `job_openings`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `title` | String | Job title |
| `department` | String | Department |
| `description` | Text | Job description |
| `status` | String | Open/closed/archived state used by the application |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

One job opening has many applications. Applications retain their job relationship even when the job is archived.

## 3. `applications`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `job_opening_id` | Integer | Foreign key to `job_openings.id`, required |
| `candidate_name` | String | Required |
| `candidate_email` | String | Required |
| `source` | String | Candidate source |
| `notes` | Text | Recruiter notes |
| `stage` | String | Current pipeline stage |
| `applied_at` | DateTime | Application timestamp |
| `updated_at` | DateTime | Last update timestamp |
| `stage_changed_at` | DateTime | Timestamp for the current stage |

One application belongs to exactly one job opening. One application can have many events, feedback entries, interviewer assignments and scheduled interviews.

## 4. `application_interviewers`

This is the join table between applications and users with the interviewer role.

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `application_id` | Integer | Foreign key to `applications.id` |
| `interviewer_id` | Integer | Foreign key to `users.id` |

This represents a many-to-many relationship: an application can have many interviewers, and an interviewer can be assigned to many applications.

The application checks that the selected user has the `interviewer` role and prevents duplicate assignments.

## 5. `feedback`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `application_id` | Integer | Foreign key to `applications.id` |
| `interviewer_id` | Integer | Foreign key to `users.id` |
| `content` | Text | Feedback text |
| `created_at` | DateTime | Submission timestamp |

One application can have many feedback records. Each feedback record belongs to one interviewer and one application.

## 6. `interview_schedules`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `application_id` | Integer | Foreign key to `applications.id` |
| `scheduled_at` | DateTime | Interview date/time |
| `notes` | Text | Optional scheduling notes |
| `created_at` | DateTime | Creation timestamp |

One application can have many scheduled interview records.

## 7. `application_events`

This is the immutable audit/history table.

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `application_id` | Integer | Foreign key to `applications.id` |
| `event_type` | String(50) | Event category |
| `old_stage` | String(30) | Previous stage when relevant |
| `new_stage` | String(30) | New stage when relevant |
| `actor_id` | Integer | Foreign key to `users.id`, nullable |
| `message` | Text | Human-readable event detail |
| `created_at` | DateTime | Event timestamp |

One application has many events. An event may have one actor. Events are append-only from the application's point of view: there is no edit/delete UI for them.

Feedback is also represented in the timeline through a feedback-submission event, while the separate `feedback` row stores the feedback record itself.

## 8. `stalled_dismissals`

| Column | Type | Notes |
|---|---|---|
| `id` | Integer | Primary key |
| `application_id` | Integer | Foreign key to `applications.id` |
| `stage` | String | Stage for which the alert was dismissed |
| `stage_started_at` | DateTime | Stage timestamp captured when dismissed |
| `dismissed_by` | Integer | Foreign key to the user who dismissed it |
| `dismissed_at` | DateTime | Dismissal timestamp |

The stage and stage-start timestamp are stored so a dismissal applies to that specific stalled state. If the application advances, the new stage has a new `stage_changed_at`, so a later stall can produce a new alert.

## Relationships

- `job_openings` → `applications`: one-to-many.
- `applications` → `application_events`: one-to-many.
- `applications` → `feedback`: one-to-many.
- `applications` → `interview_schedules`: one-to-many.
- `applications` → `stalled_dismissals`: one-to-many.
- `users` → `feedback`: one-to-many.
- `users` → `application_events`: one-to-many through `actor_id`.
- `users` ↔ `applications`: many-to-many through `application_interviewers`.

## Database constraints vs application constraints

The database handles structural constraints such as primary keys, foreign keys, required columns, and the unique user email.

Application code handles rules that depend on workflow or business meaning. Examples include:

- only recruiters can create/edit jobs and applications;
- only interviewers can be assigned to an application;
- an interviewer may only view applications assigned to them;
- applications can only be created for open jobs;
- pipeline movement must be exactly one stage at a time;
- rejected applications must be reinstated before advancing;
- rejected applications return to the exact stage from which they were rejected;
- hired applications cannot be advanced or rejected;
- bulk actions report individual successes/failures;
- stalled alerts depend on elapsed time and dismissal state.

These rules are kept in application code because they depend on the current state of multiple records and are easier to express and test in the workflow layer.

## Deliberate denormalisation

The current stage is stored directly on `applications` rather than calculated from the entire event history. Likewise, `stage_changed_at` stores when the current stage began. This makes the common list, dashboard and stalled-alert queries much cheaper than reconstructing current state from all historical events.

The event table still records the complete transition history, so the denormalised current-state fields do not replace the audit trail.


## What Would Break First at 100x the Data?

The first likely bottleneck would be the **applications listing and search workflow**. These pages combine several potentially expensive operations: searching candidate names/emails, filtering by job, stage and source, sorting, calculating the total number of matching records for pagination, and loading related application information.

At 100x the current data volume, these queries would place significantly more load on the database, particularly if users frequently perform broad text searches or sorting without suitable indexes.

The dashboard and CSV export would be the next areas to watch. Dashboard queries aggregate application data across jobs and stages, while CSV export can become expensive if a large number of rows are loaded into memory at once.

I would address these issues in stages rather than prematurely optimizing the current system:

The core schema would not need a major redesign; the main improvements would be query optimization, indexing, and more efficient data retrieval.