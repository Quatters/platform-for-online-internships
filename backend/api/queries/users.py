from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from backend.models.posts import Post
from backend.models.users import User
from backend.api.dependencies import ListPageParams
from backend.api.queries.helpers import get_instances_or_400, with_search
from backend.api.schemas import users as schemas
from backend.api.utils import hash_password


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).get(user_id)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter_by(email=email).first()


def get_users(db: Session, params: ListPageParams):
    query = with_search(
        User.email,
        User.first_name,
        User.last_name,
        User.patronymic,
        query=db.query(User),
        search=params.search,
    )
    return paginate(query, params)


def update_user(db: Session, user: User, patch_data: schemas.PatchUser):
    dict_ = patch_data.dict(exclude_unset=True)
    if 'posts' in dict_ and not user.is_admin:
        user.posts = get_instances_or_400(db, Post, dict_.pop('posts'))
    for key, value in dict_.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, user: schemas.CreateUser):
    created_user = User(
        **user.dict(exclude={'posts', 'password'}),
        password=hash_password(user.password),
    )
    if not user.is_admin:
        created_user.posts = get_instances_or_400(db, Post, user.posts)
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user
