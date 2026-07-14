# Containerized Task API

A layered FastAPI application that manages tasks.

## Architecture

This application follows a layered architecture:
- **Routes**: Handle HTTP requests, responses, status codes, dependency access, and HTTP errors.
- **Service**: Contains application and business logic.
- **Repository Interface**: A `Protocol` defining data storage operations.

### Phase 1: In-Memory Repository (Baseline)
An initial in-memory implementation of the repository was built for tests and baseline development.

### Phase 2: PostgreSQL Repository
The in-memory repository was replaced by a `PostgresTaskRepository` using `psycopg[binary]`. 
The PostgreSQL repository implements the exact same `TaskRepository` interface. **Routes and Services remained completely unchanged** during this transition. The only file modified to activate PostgreSQL was `app/dependencies.py` to wire the new repository class.

## Project Structure
```text
be-04-containerized-task-api/
├── app/
│   ├── main.py
│   ├── dependencies.py
│   ├── models/
│   │   └── task.py
│   ├── repositories/
│   │   ├── task_repository.py
│   │   ├── postgres_task_repository.py
│   │   └── in_memory_task_repository.py
│   ├── routers/
│   │   └── tasks.py
│   └── services/
│       └── task_service.py
├── sql/
│   └── 001-init.sql
├── tests/
│   └── test_tasks.py
├── .gitignore
├── .dockerignore
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Docker Prerequisites
- Docker Engine
- Docker Compose v2

## Environment Setup
1. Copy the `.env.example` file to create your local environment variables:
   ```bash
   cp .env.example .env
   ```
   (Note: `.env` is ignored by Git to avoid leaking secrets).

## Running the Complete Stack
Start the application and PostgreSQL database with:
```bash
docker compose up --build -d
```
The FastAPI app will wait for the database to become healthy. It runs on `http://127.0.0.1:8000`.

## API Endpoints & Curl Commands

**Create a task:**
```bash
curl -X POST http://127.0.0.1:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "My Docker task"}'
```

**List all tasks:**
```bash
curl http://127.0.0.1:8000/tasks
```

**Get a task by ID:**
```bash
curl http://127.0.0.1:8000/tasks/1
```

## Testing

Run unit tests locally (these still use the in-memory repository to remain fast and isolated):
```bash
python -m pytest
```

## Persistence Verification

This project uses a **named Docker volume** (`pgdata`) to ensure PostgreSQL data survives container restarts and stack recreation.

**Procedure executed to verify persistence:**
1. Started stack: `docker compose up --build -d`
2. Created a task via `POST /tasks`.
3. Verified task creation via `GET /tasks/1`.
4. Brought down the stack without removing volumes: `docker compose down`
5. Restarted the stack: `docker compose up -d`
6. Retrieved the task again via `GET /tasks/1`.

**Result:** The exact task (ID 1, same title) successfully survived the shutdown and was retrieved from the named volume.

> ⚠️ **WARNING**: Running `docker compose down -v` will explicitly delete the named volume and all stored data will be permanently lost!

## Current Limitations
- Security: Default passwords are used in `.env.example`. Do not use these in production.
- Connection Pooling is not implemented (a new connection is made per repository operation) per assignment simplifications.
