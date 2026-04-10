from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from page_builder_api.database import get_session
from page_builder_api.models import Project
from page_builder_api.schemas import ProjectPublic, ProjectSchema, ProjectsList

router = APIRouter(prefix='/projects', tags=['projects'])

T_Session = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ProjectPublic)
def create_project(
    session: T_Session,
    project: ProjectSchema,
):

    db_project = session.scalar(
        select(Project).where(Project.project_domain == project.project_domain)
    )

    if db_project:
        if db_project.project_domain == project.project_domain:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Project domain already exist.',
            )

    db_project = Project(
        user_id=project.user_id,
        project_name=project.project_name,
        project_domain=project.project_domain,
        project_type=project.project_type,
        project_category=project.project_category,
        project_description=project.project_description,
    )

    session.add(db_project)
    session.commit()
    session.refresh(db_project)

    return db_project


@router.get('/', response_model=ProjectsList)
def read_projects(
    session: T_Session,
    limit: int = 10,
    skip: int = 0,
):
    projects = session.scalars(select(Project).limit(limit).offset(skip))

    return {'projects': projects}
