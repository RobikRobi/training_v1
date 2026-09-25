from fastapi import FastAPI
from app.users.router import app as users_app
from app.projects.router import app as project_app

app = FastAPI()

app.include_router(users_app)
app.include_router(project_app)