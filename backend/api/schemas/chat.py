from datetime import datetime
from backend.api.schemas.base import BaseSchema


class SendMessage(BaseSchema):
    message: str


class FkUser(BaseSchema):
    id: int
    first_name: str
    last_name: str
    patronymic: str
    email: str


class Message(BaseSchema):
    id: int
    message: str
    recipient: FkUser
    sender: FkUser
    created_at: datetime
