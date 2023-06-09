from fastapi import Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema
from fastapi.testclient import TestClient
from backend import app
from backend.models.users import User
from backend.database import get_db
from backend.api.auth import create_access_token
from backend.api.utils import hash_password


class TestUser(BaseSchema):
    email: str
    password: str
    first_name: str = ''
    last_name: str = ''
    patronymic: str = ''
    is_admin: bool = False
    is_teacher: bool = False


test_admin = TestUser(
    email='admin@test.com',
    password='admin',
    is_admin=True,
)
test_teacher = TestUser(
    email='teacher@test.com',
    password='teacher',
    is_teacher=True,
)
test_intern = TestUser(
    email='intern@test.com',
    password='intern',
)


class TestAnonymous:
    pass


test_anonymous = TestAnonymous()


def create_user(user: TestUser, db: Session = Depends(get_db), commit=False):
    dict_ = user.dict()
    dict_.update(password=hash_password(user.password))
    db_user = User(**dict_)
    db.add(db_user)
    if commit:
        db.commit()
        db.refresh(db_user)
    return db_user


def login_as(user: TestUser | TestAnonymous) -> TestClient:
    headers = {}
    if isinstance(user, TestUser):
        token = create_access_token({'sub': user.email})
        headers['Authorization'] = f'Bearer {token}'

    with TestClient(app, headers=headers) as client:
        return client
