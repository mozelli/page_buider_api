from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from page_builder_api.database import get_session
from page_builder_api.models import User
from page_builder_api.schemas import Token
from page_builder_api.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth_Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
def login_for_access_token(session: T_Session, form_data: T_OAuth_Form):
    user = session.scalar(
        select(User).where(User.user_email == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.user_password):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Verifique seu e-mail e senha.',
        )

    access_token = create_access_token(data={'sub': user.user_email})

    return {'access_token': access_token, 'token_type': 'Bearer'}
