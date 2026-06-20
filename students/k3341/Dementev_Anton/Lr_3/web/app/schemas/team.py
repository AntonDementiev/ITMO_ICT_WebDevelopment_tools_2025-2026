from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel


class TeamCreate(SQLModel):
    name: str
    description: Optional[str] = None
    project_id: int


class TeamRead(SQLModel):
    id: int
    name: str
    description: Optional[str] = None
    project_id: int
    created_at: datetime


class TeamUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None


class TeamMemberCreate(SQLModel):
    user_id: int
    role: str = "member"


class TeamMemberRead(SQLModel):
    id: int
    team_id: int
    user_id: int
    role: str
    joined_at: datetime
