from typing import Optional

from sqlmodel import SQLModel


class SkillCreate(SQLModel):
    name: str
    level: str = "beginner"


class SkillRead(SQLModel):
    id: int
    name: str
    level: str
    user_id: int


class SkillUpdate(SQLModel):
    name: Optional[str] = None
    level: Optional[str] = None
