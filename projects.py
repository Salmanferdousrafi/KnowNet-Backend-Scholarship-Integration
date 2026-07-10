"""
Project router with strict ownership checks.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_active_user
from app.schemas.user import UserInDB
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.models.project import Project
from app.services.project_service import (
    get_project_by_id,
    list_user_projects,
    create_project,
    update_project,
    delete_project,
    verify_project_owner,
    verify_project_owner_write,
)

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("", response_model=List[ProjectOut])
async def list_projects(
    include_public: bool = False,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    """List current user's projects. Optionally include public projects from others."""
    return list_user_projects(db, current_user.id, include_public=include_public)

@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
async def create_new_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    return create_project(db, current_user.id, project_in)

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    verify_project_owner(project, current_user.id)
    return project

@router.patch("/{project_id}", response_model=ProjectOut)
async def update_project_endpoint(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    verify_project_owner_write(project, current_user.id)
    return update_project(db, project, project_in)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_endpoint(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    project = get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    verify_project_owner_write(project, current_user.id)
    delete_project(db, project)
    return None
