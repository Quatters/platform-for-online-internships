from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from backend.api.errors.errors import bad_request
from backend.models.posts import Post
from backend.models.users import User
from backend.api.dependencies import ListPageParams
from backend.api.queries.helpers import with_search
from backend.api.schemas import users as schemas


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
    if 'posts' in dict_:
        post_ids = dict_.pop('posts') or set()
        posts = set()
        if post_ids:
            posts = set(db.query(Post).filter(Post.id.in_(post_ids)).all())
        if len(post_ids) != len(posts):
            raise bad_request('Some of the posts not exist.')
        user.posts = posts
    for key, value in dict_.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
