from fastapi import HTTPException, status

from app.projects.schemas import ProjectCreate, ProjectUpdate
from app.store import next_project_id, projects
from app.users.service import get_user_or_404


def get_project_or_404(project_id: int) -> dict:
    for project in projects:
        if project["id"] == project_id:
            return project
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Project not found",
    )


def user_has_projects(user_id: int) -> bool:
    """Есть ли у пользователя проекты (нужно модулю users для 409)."""
    return any(project["owner_id"] == user_id for project in projects)


def list_projects(
    status_filter: str | None = None,
    owner_id: int | None = None,
) -> list[dict]:
    """Список проектов с фильтрацией.

    Фильтры работают и по отдельности, и одновременно:
    /projects?owner_id=2&status=active
    """
    result = projects
    if status_filter is not None:
        result = [p for p in result if p["status"] == status_filter]
    if owner_id is not None:
        result = [p for p in result if p["owner_id"] == owner_id]
    return result


def create_project(data: ProjectCreate) -> dict:
    # Обязательная проверка: владелец должен существовать.
    try:
        get_user_or_404(data.owner_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Owner not found",
        )

    project = {
        "id": next_project_id(),
        "title": data.title,
        "description": data.description,
        "owner_id": data.owner_id,
        "status": data.status,
    }
    projects.append(project)
    return project


def list_user_projects(user_id: int) -> list[dict]:
    """Все проекты конкретного пользователя (связь модулей)."""
    get_user_or_404(user_id)
    return [project for project in projects if project["owner_id"] == user_id]


def get_project_full(project_id: int) -> dict:
    """Проект вместе с вложенным объектом владельца вместо owner_id."""
    project = get_project_or_404(project_id)
    owner = get_user_or_404(project["owner_id"])
    return {
        "id": project["id"],
        "title": project["title"],
        "description": project["description"],
        "status": project["status"],
        "owner": {
            "id": owner["id"],
            "name": owner["name"],
            "email": owner["email"],
            "age": owner["age"],
        },
    }


def update_project(project_id: int, data: ProjectUpdate) -> dict:
    project = get_project_or_404(project_id)
    updates = data.model_dump(exclude_unset=True)

    # Если меняем владельца — новый владелец обязан существовать.
    new_owner_id = updates.get("owner_id")
    if new_owner_id is not None and new_owner_id != project["owner_id"]:
        get_user_or_404(new_owner_id)

    project.update(updates)
    return project


def delete_project(project_id: int) -> None:
    project = get_project_or_404(project_id)
    projects.remove(project)
