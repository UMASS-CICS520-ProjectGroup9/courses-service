
# Course Service

This Django service provides a RESTful API for searching and retrieving university course data. It supports filtering, sorting, and integration with frontend clients.

## Features
- List all courses
- Filter courses by subject, ID, title, or instructor
- Results are always sorted by `courseSubject` and `courseID`
- Designed for integration with frontend search forms and tables
- Uses JSON fixtures for initial data population

## API Endpoints
- `GET /api/courses/` — List all courses, optionally filtered by query parameters:
  - `courseSubject`: Filter by subject code (e.g., COMPSCI)
  - `courseID`: Filter by course ID
  - `title`: Filter by course title
  - `instructor`: Filter by instructor name

Example:
```
GET /api/courses/?courseSubject=COMPSCI&instructor=Smith
```

## Data Model
The `Course` model includes:
- `courseID` (AutoField, primary key)
- `courseSubject` (CharField)
- `title` (CharField)
- `instructor` (CharField)
- `credits` (IntegerField)
- `schedule` (CharField)
- `room` (CharField)
- `requirements` (TextField)
- `description` (TextField)
- `instruction_mode` (CharField)


## Requirements
Add these to `requirements.txt`:

```
Django>=5.2
djangorestframework>=3.14
```

## Setup & Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Apply migrations:
   ```bash
   python manage.py migrate
   ```
3. Load initial data:
   ```bash
   python manage.py loaddata fixtures/initial_data.json
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Development Notes
- All queries are ordered by `courseSubject` and `courseID` by default.
- API filtering is case-insensitive for string fields.
- Update `fixtures/initial_data.json` to change initial course data.
- See `base/models.py` and `api/views.py` for implementation details.

