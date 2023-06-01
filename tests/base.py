from pydantic import BaseModel as BaseSchema
from fastapi.testclient import TestClient
from backend import app


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
