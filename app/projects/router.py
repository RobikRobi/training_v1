from fastapi import APIRouter, Query, Response, status

from app.projects import service as project_service
from app.projects.schemas import (
    ProjectCreate,
    ProjectFull,
    ProjectOut,
    ProjectUpdate,
    Status,
)

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate):
    return project_service.create_project(data)


@router.get("", response_model=list[ProjectOut])
def list_projects(
    status_filter: Status | None = Query(default=None, alias="status"),
    owner_id: int | None = Query(default=None),
):
    """Фильтрация по status и/или owner_id (можно одновременно)."""
    return project_service.list_projects(status_filter, owner_id)


# ВАЖНО: /{project_id}/full объявлен до /{project_id}, чтобы путь не перехватывался.
@router.get("/{project_id}/full", response_model=ProjectFull)
def get_project_full(project_id: int):
    """Проект вместе с вложенным объектом владельца."""
    return project_service.get_project_full(project_id)


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int):
    return project_service.get_project_or_404(project_id)


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectUpdate):
    return project_service.update_project(project_id, data)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    project_service.delete_project(project_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
