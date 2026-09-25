from fastapi import HTTPException, Path
from app.users.schemas import UserSearch
from app.db import users, projects

def get_user(user_id: str) -> dict:
    for user in users:
        if str(user["id"]) == user_id:
            return user
    raise HTTPException(status_code=404, detail="Пользователь не найден")

def user_filter(search: UserSearch):
    def match(user: dict) -> bool:
        if search.name and search.name.lower() not in user["name"].lower():
            return False
        if search.email and search.email.lower() != user["email"].lower():
            return False
        if search.age is not None and search.age != user["age"]:
            return False
        return True

    return [u for u in users if match(u)]
