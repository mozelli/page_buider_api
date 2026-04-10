from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from page_builder_api.database import get_session
from page_builder_api.models import User
from page_builder_api.schemas import UserPublic, UserSchema, UsersList
from page_builder_api.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[Session, Depends(get_session)]

T_Current_User = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    db_user = session.scalar(
        select(User).where(User.user_email == user.user_email)
    )

    if db_user:
        if db_user.user_email == user.user_email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='E-mail already exist.',
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


@router.get('/', response_model=UsersList)
def read_users(
    session: T_Session,
    limit: int = 10,
    skip: int = 0,
):
    users = session.scalars(select(User).limit(limit).offset(skip))

    return {'users': users}


@router.put('/{id}', response_model=UserPublic)
def update_user(
    session: T_Session,
    current_user: T_Current_User,
    id: int,
    user: UserSchema,
):

    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Usuário não autorizado.',
        )

    current_user.user_email = user.user_email
    current_user.user_name = user.user_name
    current_user.user_password = get_password_hash(user.user_password)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{id}')
def delete_user(
    session: T_Session,
    current_user: T_Current_User,
    id: int,
):
    if current_user.id != id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Usuário não autorizado'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'Usuário excluído com sucesso!'}
