from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from backend.api.background_tasks.users import handle_user_teachers_after_post_change
from backend.api.errors.errors import not_found
from backend.api.schemas import users as schemas
from backend.api.queries import users as queries
from backend.api.auth import admin_only, admin_or_teacher_only, authenticate_user, create_access_token, current_user
from backend.database import get_db
from backend.models.users import User
from backend.api.dependencies import ListPageParams, UserListPageParams
from backend.settings import LimitOffsetPage


router = APIRouter()


def path_user(user_id: int, db: Session = Depends(get_db)):
    user = queries.get_user(db, user_id)
    if user is None:
        raise not_found()
    return user


def path_teacher(teacher_id: int, db: Session = Depends(get_db)):
    user = path_user(teacher_id, db)
    if not user.is_teacher:
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
async def get_users_me(user: Annotated[User, Depends(current_user)]):
    return user


@router.get(
    '/users',
    response_model=LimitOffsetPage[schemas.ListUser],
)
async def get_users(
    params: UserListPageParams = Depends(),
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
    background_tasks: BackgroundTasks,
    patch_data: schemas.PatchUser,
    user: User = Depends(path_user),
    db: Session = Depends(get_db),
):
    data = queries.update_user(db, user, patch_data)
    background_tasks.add_task(handle_user_teachers_after_post_change, db)
    return data


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


@router.post('/auth/register', response_model=schemas.User)
async def register(
    data: schemas.RegisterUser,
    db: Session = Depends(get_db),
):
    data.is_admin = False
    data.is_teacher = False
    return queries.create_user(db, data)


@router.get(
    '/users/{teacher_id}/assigned_interns',
    response_model=LimitOffsetPage[schemas.ListUser],
    dependencies=[Depends(admin_or_teacher_only)],
)
async def get_assigned_interns(
    db: Session = Depends(get_db),
    teacher: User = Depends(path_teacher),
    params: ListPageParams = Depends(),
):
    return queries.get_paginated_assigned_interns(db, teacher.id, params)


@router.get(
    '/users/{teacher_id}/interns_with_stats',
    response_model=LimitOffsetPage[schemas.InternWithStats],
    dependencies=[Depends(admin_or_teacher_only)],
)
async def get_best_interns(
    db: Session = Depends(get_db),
    teacher: User = Depends(path_teacher),
    params: ListPageParams = Depends(),
):
    return queries.get_interns_with_stats(db, teacher, params)


@router.get(
    '/users/{teacher_id}/assigned_interns/{intern_id}',
    response_model=schemas.User,
    dependencies=[Depends(admin_or_teacher_only)],
)
async def get_one_assigned_intern(
    intern_id: int,
    db: Session = Depends(get_db),
    teacher: User = Depends(path_teacher),
):
    return queries.get_assigned_intern(db, teacher.id, intern_id)


@router.delete(
    '/users/{intern_id}',
    status_code=204,
    dependencies=[Depends(admin_or_teacher_only)],
)
async def unassign_intern(
    intern_id: int,
    db: Session = Depends(get_db),
):
    queries.unassign_intern(db, intern_id)
    return {}


@router.put(
    '/users/{teacher_id}/assigned_interns',
    response_model=schemas.AssignInterns,
    dependencies=[Depends(admin_or_teacher_only)],
)
async def assign_interns(
    data: schemas.AssignInterns,
    teacher: User = Depends(path_teacher),
    db: Session = Depends(get_db),
):
    queries.assign_interns(db, teacher, data.interns)
    return data


@router.get(
    '/users/{teacher_id}/suitable_for_assign_interns',
    response_model=LimitOffsetPage[schemas.FkUser],
    dependencies=[Depends(admin_or_teacher_only)],
)
async def get_suitable_for_assign_interns(
    db: Session = Depends(get_db),
    teacher: User = Depends(path_teacher),
    params: ListPageParams = Depends(),
):
    return queries.get_suitable_for_assign_interns(db, teacher, params)
