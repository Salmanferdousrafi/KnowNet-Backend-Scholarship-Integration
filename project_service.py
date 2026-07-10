"""
Project CRUD with strict ownership checks.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def get_project_by_id(db: Session, project_id: int) -> Optional[Project]:
    return db.query(Project).filter(Project.id == project_id).first()

def list_user_projects(db: Session, user_id: int, include_public: bool = False) -> List[Project]:
    query = db.query(Project).filter(Project.owner_id == user_id)
    if include_public:
        query = query.union(
            db.query(Project).filter(Project.is_public == True, Project.owner_id != user_id)
        )
    return query.order_by(Project.updated_at.desc()).all()

def create_project(db: Session, user_id: int, project_in: ProjectCreate) -> Project:
    db_project = Project(
        owner_id=user_id,
        title=project_in.title,
        description=project_in.description,
        is_public=project_in.is_public,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(db: Session, project: Project, project_in: ProjectUpdate) -> Project:
    update_data = project_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()

def verify_project_owner(project: Project, user_id: int) -> None:
    """Raise 403 if user does not own the project and it's not public."""
    if project.owner_id != user_id and not project.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this project"
        )

def verify_project_owner_write(project: Project, user_id: int) -> None:
    """Raise 403 if user does not own the project (write operations)."""
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to modify this project"
        )
