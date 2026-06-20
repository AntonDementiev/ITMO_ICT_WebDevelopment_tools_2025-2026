from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models.project import Project
from app.models.team import Team, TeamMember
from app.models.user import User
from app.schemas.team import TeamCreate, TeamMemberCreate, TeamMemberRead, TeamRead, TeamUpdate

router = APIRouter(prefix="/teams", tags=["Команды"])


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(
    data: TeamCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Team:
    project = session.get(Project, data.project_id)
    if project is None or project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не владелец проекта")
    team = Team(**data.model_dump())
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.get("/", response_model=List[TeamRead])
def list_teams(session: Session = Depends(get_session)) -> List[Team]:
    return session.exec(select(Team)).all()


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, session: Session = Depends(get_session)) -> Team:
    team = session.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    return team


@router.patch("/{team_id}", response_model=TeamRead)
def update_team(
    team_id: int,
    data: TeamUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Team:
    team = session.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    project = session.get(Project, team.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не владелец проекта")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(team, key, value)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    team = session.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    project = session.get(Project, team.project_id)
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Вы не владелец проекта")
    session.delete(team)
    session.commit()


@router.post("/{team_id}/members", response_model=TeamMemberRead, status_code=status.HTTP_201_CREATED)
def add_member(
    team_id: int,
    data: TeamMemberCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TeamMember:
    team = session.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    existing = session.exec(
        select(TeamMember).where(TeamMember.team_id == team_id, TeamMember.user_id == data.user_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже в команде")
    member = TeamMember(team_id=team_id, user_id=data.user_id, role=data.role)
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


@router.get("/{team_id}/members", response_model=List[TeamMemberRead])
def list_members(team_id: int, session: Session = Depends(get_session)) -> List[TeamMember]:
    return session.exec(select(TeamMember).where(TeamMember.team_id == team_id)).all()


@router.delete("/{team_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member(
    team_id: int,
    member_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    member = session.get(TeamMember, member_id)
    if member is None or member.team_id != team_id:
        raise HTTPException(status_code=404, detail="Участник не найден")
    session.delete(member)
    session.commit()
