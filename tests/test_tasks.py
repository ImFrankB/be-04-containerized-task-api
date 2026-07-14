import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_task_service
from app.services.task_service import TaskService
from app.repositories.in_memory_task_repository import InMemoryTaskRepository

@pytest.fixture
def test_client():
    # Provide a fresh repository for each test
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    app.dependency_overrides[get_task_service] = lambda: service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

def test_create_task(test_client):
    response = test_client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data

def test_create_task_empty_title(test_client):
    response = test_client.post("/tasks", json={"title": ""})
    assert response.status_code == 422

def test_create_task_whitespace_title(test_client):
    response = test_client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422

def test_get_tasks(test_client):
    test_client.post("/tasks", json={"title": "Task 1"})
    test_client.post("/tasks", json={"title": "Task 2"})
    
    response = test_client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_get_task_by_id(test_client):
    create_response = test_client.post("/tasks", json={"title": "Task 1"})
    task_id = create_response.json()["id"]
    
    response = test_client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Task 1"

def test_get_task_not_found(test_client):
    response = test_client.get("/tasks/999")
    assert response.status_code == 404
