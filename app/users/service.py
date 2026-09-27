from fastapi import HTTPException, status

from app.store import next_user_id, users
from app.users.schemas import UserCreate, UserUpdate


def get_user_or_404(user_id: int) -> dict:
    """Возвращает пользователя по id или 404 (используется и проектами)."""
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


def list_users() -> list[dict]:
    return users


def create_user(data: UserCreate) -> dict:
    user = {
        "id": next_user_id(),
        "name": data.name,
        "email": str(data.email),
        "age": data.age,
    }
    users.append(user)
    return user


def search_users(name: str | None = None) -> list[dict]:
    """Поиск по подстроке имени, без учёта регистра.

    ?name=den найдёт Denis, DENIS и denis.
    Без параметра возвращает всех пользователей.
    """
    if name is None:
        return users
    needle = name.lower()
    return [user for user in users if needle in user["name"].lower()]


def update_user(user_id: int, data: UserUpdate) -> dict:
    user = get_user_or_404(user_id)
    updates = data.model_dump(exclude_unset=True)
    if "email" in updates and updates["email"] is not None:
        updates["email"] = str(updates["email"])
    user.update(updates)
    return user


def delete_user(user_id: int) -> None:
    """Удаляет пользователя.

    Если у пользователя есть проекты — удалять нельзя, 409 Conflict:
    сначала он должен удалить свои проекты.
    """
    from app.projects import service as project_service

    user = get_user_or_404(user_id)

    if project_service.user_has_projects(user_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has projects",
        )

    users.remove(user)
