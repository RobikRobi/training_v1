from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from uuid import uuid4
from app.db import users, projects
from app.users.schemas import UserCreate, UserShow, UserUpdate, UserSearch
from app.users.service import get_user, user_filter

app = APIRouter(prefix="/users", tags=["Users"])

@app.post("/register", response_model=UserShow)
def register_user(data:UserCreate):
    id = str(uuid4())
    name = data.name
    email = data.email
    age = data.age

    user = {
            'id': id, 
            'name': name, 
            'email': email, 
            'age': age
            }
    users.append(user)
    return users[-1]

@app.get("/all_users")
def all_users():
    return users

@app.get("/search", response_model=list[UserShow])
def search_users(search: Annotated[UserSearch, Depends()]):
    return user_filter(search)

@app.get("/{user_id}", response_model=UserShow)
def me(me=Depends(get_user)):
    return me

@app.put("/{user_id}", response_model=UserShow)
def update_user(data: UserUpdate, user: dict = Depends(get_user)):
    updates = data.model_dump(exclude_unset=True)
    user.update(updates)
    return user

@app.delete("/{user_id}")
def delete_user(user: dict = Depends(get_user)):
    users.remove(user)
    return {"message": "Пользователь успешно удалён."}

