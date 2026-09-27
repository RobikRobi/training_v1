from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(ge=14)


class UserCreate(UserBase):
    """Тело для POST /users — id генерирует сервер."""


class UserUpdate(BaseModel):
    """Тело для PUT /users/{user_id}.

    Все поля опциональны: обновляется только то, что прислали.
    """

    name: str | None = None
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=14)


class UserOut(UserBase):
    """Ответ пользователя с id."""

    id: int
