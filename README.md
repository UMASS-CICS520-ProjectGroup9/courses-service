# Courses Service

This Django RESTful microservice provides endpoints for searching, retrieving, creating, and deleting university course data. It supports filtering, JWT-based authentication, and role-based permissions for integration with a larger academic platform.

## Features
- List all courses
- Filter by subject, ID, title, or instructor (case-insensitive)
- Create and delete courses (with role-based access)
- Automatically creates/deletes associated discussions via external service
- JWT authentication (integrates with userauthen-service)
- Uses JSON fixtures for initial data
- Unit tests for API endpoints

## API Endpoints
All endpoints are under `/api/`:

- `GET /api/` — API overview
- `GET /api/courses/` — List all courses, filterable by:
  - `courseSubject`, `courseID`, `title`, `instructor`
- `POST /api/courses/create/` — Create a new course (STAFF/ADMIN only)
- `DELETE /api/courses/<courseSubject>/<courseID>/delete/` — Delete a course (STAFF/ADMIN/owner)

Example filter:
```http
GET /api/courses/?courseSubject=COMPSCI&instructor=Smith
```

## Data Model
`base/models.py` defines the `Course` model:
- `courseID` (IntegerField, primary key)
- `creator_id` (IntegerField, user ID)
- `courseSubject` (CharField)
- `title` (CharField)
- `instructor` (CharField)
- `credits` (IntegerField)
- `schedule` (CharField)
- `room` (CharField)
- `requirements` (TextField)
- `description` (TextField)
- `instruction_mode` (CharField)

## Authentication & Permissions
- JWT authentication via `ExternalJWTAuthentication` (see `coursesService/authentication.py`)
- Roles: STUDENT, STAFF, ADMIN
- Permissions:
  - List/search: STUDENT+
  - Create/delete: STAFF/ADMIN (delete also allows owner)

## Setup & Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Apply migrations:
   ```bash
   python coursesService/manage.py migrate
   ```
3. Load initial data:
   ```bash
   python coursesService/manage.py loaddata fixtures/initial_data.json
   ```
4. Run the development server:
   ```bash
   python coursesService/manage.py runserver
   ```

## Requirements
See `requirements.txt` for full list. Key packages:
```
Django>=5.2
djangorestframework>=3.14
djangorestframework_simplejwt
```

## Testing
Unit tests are in `base/tests.py`:
```bash
python coursesService/manage.py test base
```

## Development Notes
- All queries are ordered by `courseSubject` and `courseID` by default.
- API filtering is case-insensitive for string fields.
- Update `fixtures/initial_data.json` to change initial course data.
- See `base/models.py`, `api/views.py`, and `api/permissions.py` for implementation details.

## Project Structure
- `coursesService/` — Django project root
  - `api/` — API views, serializers, permissions, urls
  - `base/` — Models, tests, migrations
  - `coursesService/` — Project settings, authentication, root urls
  - `fixtures/` — Initial data
  - `manage.py` — Django management script

---
For integration details, see the main project documentation.

