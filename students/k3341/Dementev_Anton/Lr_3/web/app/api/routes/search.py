from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.skill import Skill
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter(prefix="/search", tags=["Поиск"])


@router.get("/users", response_model=List[UserRead])
def search_users(
    skill: Optional[str] = Query(None, description="Фильтр по навыку"),
    min_experience: Optional[int] = Query(None, description="Мин. лет опыта"),
    session: Session = Depends(get_session),
) -> List[User]:
    stmt = select(User).where(User.is_active == True)
    if skill:
        stmt = stmt.join(Skill).where(Skill.name.ilike(f"%{skill}%"))
    if min_experience is not None:
        stmt = stmt.where(User.experience_years >= min_experience)
    return session.exec(stmt).all()
