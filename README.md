# Crehana Task API

A REST API to manage task lists and tasks. Built with FastAPI and PostgreSQL.

---

## Requirements

- Docker
- Docker Compose

---

## Setup

### 1. Create the `.env` file

Create a file called `.env` in the root of the project with this content:

```env
DATABASE_URL=postgresql://crehana:crehana@db:5432/crehana
SECRET_KEY=your-secret-key-here
POSTGRES_USER=crehana
POSTGRES_PASSWORD=crehana
POSTGRES_DB=crehana
```

### 2. Start the project

```bash
docker compose up --build
```

The API will be available at: http://localhost:8000

The API docs (Swagger) will be available at: http://localhost:8000/docs

### 3. Stop the project

```bash
docker compose down
```

If you want to also delete the database data:

```bash
docker compose down -v
```

---

## How to use the API

### Step 1 — Register a user

```
POST /auth/register
```

```json
{
  "username": "myuser",
  "email": "myuser@example.com",
  "password": "mypassword"
}
```

### Step 2 — Login

```
POST /auth/login
```

```json
{
  "username": "myuser",
  "password": "mypassword"
}
```

The response will include an `access_token`. You need to send this token in the `Authorization` header for all other requests:

```
Authorization: Bearer <your_token_here>
```

### Step 3 — Create a task list

```
POST /lists/
```

```json
{
  "title": "My list",
  "description": "Optional description"
}
```

### Step 4 — Create a task

```
POST /lists/{task_list_id}/tasks/
```

```json
{
  "title": "My task",
  "description": "Optional description",
  "priority": "high",
  "assigned_to": 1
}
```

`priority` can be: `low`, `medium`, or `high`. Default is `medium`.

`assigned_to` is optional. It is the ID of the user you want to assign the task to.

### Step 5 — Change the status of a task

```
PATCH /lists/{task_list_id}/tasks/{task_id}/status
```

```json
{
  "status": "in_progress"
}
```

`status` can be: `pending`, `in_progress`, or `done`.

---

## Run the tests

The tests use SQLite (in memory), so they do not need the database to be running.

```bash
docker compose exec api pytest tests/ -v
```

To see the code coverage:

```bash
docker compose exec api pytest tests/ -v --cov=. --cov-report=term-missing
```

---

## Run the linters

All commands run inside the Docker container.

### Check code style with flake8

```bash
docker compose exec api flake8 .
```

### Format the code with black

```bash
docker compose exec api black .
```

### Sort the imports with isort

```bash
docker compose exec api isort .
```

### Run all three together

```bash
docker compose exec api black . && docker compose exec api isort . && docker compose exec api flake8 .
```

---

## Project structure

```
.
├── api/                  # HTTP layer (routes, schemas, dependencies)
│   ├── auth.py
│   ├── task_lists.py
│   ├── tasks.py
│   ├── deps.py
│   ├── schemas.py
│   └── main.py
├── application/          # Business logic (services)
│   ├── auth_service.py
│   ├── task_list_service.py
│   └── task_service.py
├── domain/               # Core models and exceptions
│   ├── models.py
│   └── exceptions.py
├── infrastructure/       # Database, repositories, config
│   ├── models_orm.py
│   ├── database.py
│   ├── config.py
│   ├── security.py
│   ├── notifications.py
│   └── repositories/
├── tests/                # Unit tests
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_task_lists.py
│   └── test_tasks.py
├── .flake8
├── pytest.ini
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
