from typing import List, Optional, Protocol
from app.models.task import Task, TaskCreate

class TaskRepository(Protocol):
    def create(self, task: TaskCreate) -> Task:
        ...

    def list_all(self) -> List[Task]:
        ...

    def get_by_id(self, task_id: int) -> Optional[Task]:
        ...
