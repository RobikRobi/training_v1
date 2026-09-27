from typing import Literal

from pydantic import BaseModel


Status = Literal["active", "paused", "completed"]


class ProjectBase(BaseModel):
    title: str
    description: str
    status: Status


class ProjectCreate(ProjectBase):
    owner_id: int


class ProjectUpdate(BaseModel):
    """Тело для PUT /projects/{project_id} — partial update."""

    title: str | None = None
    description: str | None = None
    owner_id: int | None = None
    status: Status | None = None


class ProjectOut(ProjectBase):
    id: int
    owner_id: int


class UserBrief(BaseModel):
    """Короткое представление владельца для вложенных ответов."""

    id: int
    name: str
    email: str
    age: int


class ProjectFull(BaseModel):
    """Проект с вложенным объектом владельца вместо owner_id."""

    id: int
    title: str
    description: str
    status: Status
    owner: UserBrief
