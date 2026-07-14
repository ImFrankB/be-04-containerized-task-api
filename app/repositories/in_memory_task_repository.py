from datetime import datetime, timezone
from typing import List, Optional
from app.models.task import Task, TaskCreate
from app.repositories.task_repository import TaskRepository

class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def create(self, task: TaskCreate) -> Task:
        new_task = Task(
            id=self.next_id,
            title=task.title,
            completed=task.completed,
            created_at=datetime.now(timezone.utc)
        )
        self.tasks.append(new_task)
        self.next_id += 1
        return new_task

    def list_all(self) -> List[Task]:
        return list(self.tasks)

    def get_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
