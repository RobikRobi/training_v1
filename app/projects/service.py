from fastapi import HTTPException
from app.db import projects

def get_project(project_id: str):
    for project in projects:
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail="Проект не найден")