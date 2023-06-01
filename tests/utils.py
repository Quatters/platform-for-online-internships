from fastapi.testclient import TestClient
from backend.api.auth import authenticate_user
from backend import app
from backend.database import get_db
from create_user import create_user
from .base import TestUser


def login_as(user: TestUser):
    token = authenticate_user(next(get_db()), user.email, user.password)
    c = TestClient(app, headers={
        'Authorization': f'Bearer {token}'
    })
    return c
