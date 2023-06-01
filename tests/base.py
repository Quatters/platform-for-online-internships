from fastapi import Depends
from pydantic import BaseModel as BaseSchema
from fastapi.testclient import TestClient
from backend import app
from backend.models.users import User
from backend.database import get_db
from backend.api.auth import create_access_token, hash_password


client = TestClient(app)


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
)
test_teacher = TestUser(
    email='teacher@test.com',
    password='teacher',
)
test_intern = TestUser(
    email='intern@test.com',
    password='intern',
)


def create_user(user: TestUser, db = Depends(get_db), commit=False):
    dict_ = user.dict()
    dict_.update(password=hash_password(user.password))
    db_user = User(**dict_)
    db.add(db_user)
    if commit:
        db.commit()


def login_as(user: TestUser) -> TestClient:
    token = create_access_token({'sub': user.email})
    return TestClient(app, headers={
        'Authorization': f'Bearer {token}'
    })
