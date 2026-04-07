from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from page_builder_api.database import get_session
from page_builder_api.models import Project, User
from page_builder_api.schemas import (
    ProjectPublic,
    ProjectSchema,
    ProjectsList,
    Token,
    UserPublic,
    UserSchema,
    UsersList,
)
from page_builder_api.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI()


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.user_email == user.user_email))

    if db_user:
        if db_user.user_email == user.user_email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='E-mail already exist.'
            )

    db_user: UserSchema = User(
        user_name=user.user_name,
        user_email=user.user_email,
        user_password=get_password_hash(user.user_password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UsersList)
def read_users(
    limit: int = 10,
    skip: int = 0,
    session: Session = Depends(get_session),
):
    users = session.scalars(select(User).limit(limit).offset(skip))

    return {'users': users}


@app.put('/users/{id}', response_model=UserPublic)
def update_user(
    id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):

    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Usuário não autorizado.'
        )

    current_user.user_email = user.user_email
    current_user.user_name = user.user_name
    current_user.user_password = get_password_hash(user.user_password)

    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{id}')
def delete_user(
    id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Usuário não autorizado'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Usuário excluído com sucesso!'}


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.user_email == form_data.username))

    if not user or not verify_password(form_data.password, user.user_password):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Verifique seu e-mail e senha.'
        )

    access_token = create_access_token(data={'sub': user.user_email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@app.post('/projects/', status_code=HTTPStatus.CREATED, response_model=ProjectPublic)
def create_project(project: ProjectSchema, session: Session = Depends(get_session)):

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


@app.get('/projects/', response_model=ProjectsList)
def read_projects(
    limit: int = 10, skip: int = 0, session: Session = Depends(get_session)
):
    projects = session.scalars(select(Project).limit(limit).offset(skip))

    return {'projects': projects}
