from fastapi import FastAPI

from app.projects.router import router as projects_router
from app.users.router import router as users_router

app = FastAPI(title="Users & Projects API")

app.include_router(users_router)
app.include_router(projects_router)
