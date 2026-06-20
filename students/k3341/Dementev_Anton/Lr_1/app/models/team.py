from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User


class TeamBase(SQLModel):
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)


class Team(TeamBase, table=True):
    __tablename__ = "team"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    project: Optional["Project"] = Relationship(back_populates="teams")
    members: List["TeamMember"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class TeamMemberBase(SQLModel):
    role: str = Field(default="member", max_length=50)


class TeamMember(TeamMemberBase, table=True):
    __tablename__ = "team_member"

    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")
    user_id: int = Field(foreign_key="user.id")
    joined_at: datetime = Field(default_factory=datetime.utcnow)

    team: Optional["Team"] = Relationship(back_populates="members")
    user: Optional["User"] = Relationship(back_populates="team_memberships")
