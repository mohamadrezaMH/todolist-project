from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..dependencies.database import get_db
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectStats
from ...repositories.project_repository import ProjectRepository
from ...repositories.task_repository import TaskRepository
from ...services.project_service import ProjectService
from ...exceptions.service_exceptions import ValidationError
from ...exceptions.repository_exceptions import NotFoundError, DuplicateError

router = APIRouter()


def get_project_service(db: Session = Depends(get_db)):
    """Dependency for project service"""
    project_repo = ProjectRepository(db)
    task_repo = TaskRepository(db)
    return ProjectService(project_repo, task_repo)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service)
):
    """Create a new project"""
    try:
        project = project_service.create_project(
            name=project_data.name,
            description=project_data.description
        )
        return project
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    project_service: ProjectService = Depends(get_project_service)
):
    """Get all projects"""
    return project_service.get_all_projects()


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """Get a specific project by ID"""
    project = project_service.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service)
):
    """Update a project"""
    try:
        project = project_service.update_project(
            project_id=project_id,
            name=project_data.name or "",
            description=project_data.description or ""
        )
        return project
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    except DuplicateError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """Delete a project"""
    success = project_service.delete_project(project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )


@router.get("/{project_id}/stats", response_model=ProjectStats)
async def get_project_statistics(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """Get statistics for a project"""
    try:
        stats = project_service.get_project_stats(project_id)
        return stats
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))