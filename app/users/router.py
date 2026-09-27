from fastapi import APIRouter, Query, Response, status

from app.projects import service as project_service
from app.projects.schemas import ProjectOut
from app.users import service as user_service
from app.users.schemas import UserCreate, UserOut, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate):
    return user_service.create_user(data)


@router.get("", response_model=list[UserOut])
def list_users():
    return user_service.list_users()


# ВАЖНО: /search объявлен до /{user_id}, иначе "search" ушёл бы в путь-параметр.
@router.get("/search", response_model=list[UserOut])
def search_users(name: str | None = Query(default=None)):
    return user_service.search_users(name)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    return user_service.get_user_or_404(user_id)


@router.get("/{user_id}/projects", response_model=list[ProjectOut])
def list_user_projects(user_id: int):
    """Связь модулей: все проекты пользователя."""
    return project_service.list_user_projects(user_id)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate):
    return user_service.update_user(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    user_service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
