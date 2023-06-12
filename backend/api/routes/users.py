from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.api.errors.errors import not_found
from backend.api.schemas import users as schemas
from backend.api.queries import users as queries
from backend.api.auth import admin_only, authenticate_user, create_access_token, get_current_user
from backend.database import get_db
from backend.models.users import User
from backend.api.dependencies import ListPageParams
from backend.settings import LimitOffsetPage


router = APIRouter()


def path_user(user_id: int, db: Session = Depends(get_db)):
    user = queries.get_user(db, user_id)
    if user is None:
        raise not_found()
    return user


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


@router.get(
    '/users',
    response_model=LimitOffsetPage[schemas.ListUser],
)
async def get_users(
    params: ListPageParams = Depends(),
    db: Session = Depends(get_db),
):
    return queries.get_users(db, params)


@router.get(
    '/users/{user_id}',
    response_model=schemas.User,
)
async def get_user(
    user: User = Depends(path_user),
):
    return user


@router.patch(
    '/users/{user_id}',
    response_model=schemas.User,
    dependencies=[Depends(admin_only)],
)
async def patch_user(
    patch_data: schemas.PatchUser,
    user: User = Depends(path_user),
    db: Session = Depends(get_db),
):
    return queries.update_user(db, user, patch_data)


@router.post(
    '/users',
    response_model=schemas.User,
    dependencies=[Depends(admin_only)],
)
async def create_user(
    data: schemas.CreateUser,
    db: Session = Depends(get_db),
):
    return queries.create_user(db, data)
