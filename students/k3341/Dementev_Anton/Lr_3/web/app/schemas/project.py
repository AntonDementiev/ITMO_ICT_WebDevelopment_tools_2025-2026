from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class ProjectCreate(SQLModel):
    title: str
    description: Optional[str] = None
    status: str = "open"
    deadline: Optional[datetime] = None


class ProjectRead(SQLModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    deadline: Optional[datetime] = None
    owner_id: int
    created_at: datetime


class ProjectUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None
