from pydantic import BaseModel
from uuid import uuid4
# from app.projects.project_enum import Status


class ProjectCreate(BaseModel):
    title: str
    description: str
    owner_id: str
    status: str

class ProjectShow(BaseModel):
    id: str
    title: str
    description: str
    owner_id: str
    status: str