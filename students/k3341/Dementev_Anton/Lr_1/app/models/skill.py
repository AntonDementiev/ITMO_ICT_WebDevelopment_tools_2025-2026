from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class SkillBase(SQLModel):
    name: str = Field(max_length=100)
    level: str = Field(default="beginner", max_length=50)


class Skill(SkillBase, table=True):
    __tablename__ = "skill"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="skills")
