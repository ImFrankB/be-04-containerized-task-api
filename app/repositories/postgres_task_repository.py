import os
from typing import List, Optional
import psycopg
from psycopg.rows import dict_row
from app.models.task import Task, TaskCreate
from app.repositories.task_repository import TaskRepository

class PostgresTaskRepository(TaskRepository):
    def __init__(self):
        self.db_url = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tasks_db")

    def _get_connection(self):
        return psycopg.connect(self.db_url, row_factory=dict_row)

    def create(self, task: TaskCreate) -> Task:
        query = """
            INSERT INTO tasks (title, completed)
            VALUES (%s, %s)
            RETURNING id, title, completed, created_at;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (task.title, task.completed))
                row = cur.fetchone()
                conn.commit()
                return Task(**row)

    def list_all(self) -> List[Task]:
        query = "SELECT id, title, completed, created_at FROM tasks ORDER BY id ASC;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                return [Task(**row) for row in rows]

    def get_by_id(self, task_id: int) -> Optional[Task]:
        query = "SELECT id, title, completed, created_at FROM tasks WHERE id = %s;"
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (task_id,))
                row = cur.fetchone()
                if row:
                    return Task(**row)
                return None
