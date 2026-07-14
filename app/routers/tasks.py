from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.task import Task, TaskCreate
from app.services.task_service import TaskService
from app.dependencies import get_task_service

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.post("", response_model=Task, status_code=201)
def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    try:
        return service.create_task(task)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("", response_model=List[Task])
def get_tasks(service: TaskService = Depends(get_task_service)):
    return service.get_all_tasks()

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
