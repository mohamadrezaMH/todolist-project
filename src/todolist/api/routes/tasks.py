from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate
from ...repositories.task_repository import TaskRepository
from ...repositories.project_repository import ProjectRepository
from ...services.task_service import TaskService
from ...services.project_service import ProjectService
from ...exceptions.service_exceptions import ValidationError
from ...exceptions.repository_exceptions import NotFoundError

router = APIRouter()


def get_task_service(db: Session = Depends(get_db)):
    """Dependency for task service"""
    task_repo = TaskRepository(db)
    return TaskService(task_repo)


def get_project_service(db: Session = Depends(get_db)):
    """Dependency for project service"""
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return ProjectService(project_repo, task_repo)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """Create a new task"""
    try:
        # Check if project exists
        if not project_service.project_exists(task_data.project_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with id {task_data.project_id} not found"
            )
        
        task = task_service.create_task(
            project_id=task_data.project_id,
            title=task_data.title,
            description=task_data.description,
            deadline=task_data.deadline
        )
        return task
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    project_id: int = Query(None, description="Filter by project ID"),
    status: str = Query(None, description="Filter by status", pattern="^(todo|doing|done)$"),
    task_service: TaskService = Depends(get_task_service)
):
    """Get tasks with optional filtering"""
    if project_id is not None:
        tasks = task_service.get_tasks_by_project(project_id)
    else:
        # For simplicity, get all tasks if no filter
        # In real app, you might want pagination here
        tasks = task_service.task_repo.get_all()
    
    if status:
        tasks = [t for t in tasks if t.status == status]
    
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """Get a specific task by ID"""
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    """Update a task"""
    try:
        # Get current task to preserve fields not being updated
        current_task = task_service.get_task(task_id)
        if not current_task:
            raise NotFoundError("Task", task_id)
        
        task = task_service.update_task(
            task_id=task_id,
            title=task_data.title or current_task.title,
            description=task_data.description or current_task.description,
            status=task_data.status or current_task.status,
            deadline=task_data.deadline if task_data.deadline is not None else current_task.deadline
        )
        return task
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    status_update: TaskStatusUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    """Update only task status"""
    try:
        task = task_service.change_task_status(task_id, status_update.status)
        return task
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """Delete a task"""
    success = task_service.delete_task(task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


@router.get("/overdue/", response_model=List[TaskResponse])
async def get_overdue_tasks(
    project_id: int = Query(None, description="Filter by project ID"),
    task_service: TaskService = Depends(get_task_service)
):
    """Get overdue tasks"""
    return task_service.get_overdue_tasks(project_id)