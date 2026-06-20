from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.core.database import get_session
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["Проекты"])


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Project:
    project = Project(**data.model_dump(), owner_id=current_user.id)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("/", response_model=List[ProjectRead])
def list_projects(
    status_filter: Optional[str] = Query(None, alias="status"),
    session: Session = Depends(get_session),
) -> List[Project]:
    stmt = select(Project)
    if status_filter:
        stmt = stmt.where(Project.status == status_filter)
    return session.exec(stmt).all()


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, session: Session = Depends(get_session)) -> Project:
    project = session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Проект не найден")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Project:
    project = session.get(Project, project_id)
    if project is None or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Проект не найден")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> None:
    project = session.get(Project, project_id)
    if project is None or project.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Проект не найден")
    session.delete(project)
    session.commit()
