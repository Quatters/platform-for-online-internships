from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.api.schemas import users as schemas
from backend.api.auth import authenticate_user, create_access_token, get_current_user
from backend.database import get_db


router = APIRouter()


@router.post('/auth/token', response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return schemas.Token(
        access_token=create_access_token(data={'sub': user.email}),
        token_type='bearer',
    )


@router.get('/users/me', response_model=schemas.User)
async def get_users_me(user: Annotated[schemas.User, Depends(get_current_user)]):
    return user
