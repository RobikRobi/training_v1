from fastapi import APIRouter, Depends
from uuid import uuid4
from app.db import users, projects
from app.users.service import get_user
from app.projects.schemas import ProjectCreate, ProjectShow
from app.projects.service import get_project

app = APIRouter(prefix="/projects", tags=["Projects"])

@app.post("/create")
def create_project(project: ProjectCreate):
    id = str(uuid4())
    title = project.title
    description = project.description
    owner_id = project.owner_id 
    owner_id = project.owner_id
    status = project.status
    new_project = {
        "id": id,
        "title": title,
        "description": description,
        "owner_id": owner_id,
        "status": status
    }
    projects.append(new_project)
    return new_project

@app.get("/all")
def get_all_projects():
    return projects

@app.get("/{project_id}", response_model=ProjectShow)
def get_project(project_id: str):
    project = Depends(get_project)
    return project
