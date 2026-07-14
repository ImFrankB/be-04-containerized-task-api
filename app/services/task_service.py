from typing import List, Optional
from app.models.task import Task, TaskCreate
from app.repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task_create: TaskCreate) -> Task:
        if not task_create.title or not task_create.title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        
        return self.repository.create(task_create)

    def get_all_tasks(self) -> List[Task]:
        return self.repository.list_all()

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.repository.get_by_id(task_id)
