from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models.skill import Skill
from app.models.user import User
from app.schemas.skill import SkillCreate, SkillRead, SkillUpdate

router = APIRouter(prefix="/skills", tags=["Навыки"])


@router.post("/", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill(
    data: SkillCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Skill:
    skill = Skill(**data.model_dump(), user_id=current_user.id)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill


@router.get("/", response_model=List[SkillRead])
def list_my_skills(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> List[Skill]:
    return session.exec(select(Skill).where(Skill.user_id == current_user.id)).all()


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    skill = session.get(Skill, skill_id)
    if skill is None or skill.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Навык не найден")
    session.delete(skill)
    session.commit()


@router.patch("/{skill_id}", response_model=SkillRead)
def update_skill(
    skill_id: int,
    data: SkillUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Skill:
    skill = session.get(Skill, skill_id)
    if skill is None or skill.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Навык не найден")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(skill, key, value)
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill
