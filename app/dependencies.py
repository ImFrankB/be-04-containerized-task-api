from app.repositories.in_memory_task_repository import InMemoryTaskRepository
from app.services.task_service import TaskService

repository = InMemoryTaskRepository()

def get_task_service() -> TaskService:
    return TaskService(repository)
