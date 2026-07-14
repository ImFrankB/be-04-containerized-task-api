# Containerized Task API

A layered FastAPI application that manages tasks.

## Architecture

This application follows a layered architecture:
- **Routes**: Handle HTTP requests, responses, status codes, dependency access, and HTTP errors.
- **Service**: Contains application and business logic.
- **Repository Interface**: A `Protocol` defining data storage operations.
- **In-Memory Repository**: A simple list-based implementation of the repository interface used as a baseline.

Currently, data is stored in memory. The repository interface allows for replacing this implementation (e.g., with PostgreSQL) without modifying the routes or services.

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # source venv/bin/activate    # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

Start the local server:
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.
Swagger documentation is available at `http://127.0.0.1:8000/docs`.

## Example `curl` Commands

**Create a task:**
```bash
curl -X POST http://127.0.0.1:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "My first task"}'
```

**List all tasks:**
```bash
curl http://127.0.0.1:8000/tasks
```

**Get a single task by ID:**
```bash
curl http://127.0.0.1:8000/tasks/1
```

## Testing

Run tests with `pytest`:
```bash
pytest
```
