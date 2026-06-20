from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.team import Team
    from app.models.user import User


class ProjectBase(SQLModel):
    title: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="open", max_length=50)
    deadline: Optional[datetime] = Field(default=None)


class Project(ProjectBase, table=True):
    __tablename__ = "project"

    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: Optional["User"] = Relationship(back_populates="owned_projects")
    teams: List["Team"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
