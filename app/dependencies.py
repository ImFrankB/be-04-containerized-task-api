from app.repositories.postgres_task_repository import PostgresTaskRepository
from app.services.task_service import TaskService

repository = PostgresTaskRepository()

def get_task_service() -> TaskService:
    return TaskService(repository)
