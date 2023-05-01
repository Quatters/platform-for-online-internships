from sqlalchemy import Column, String, Boolean, CheckConstraint
from sqlalchemy.sql import expression
from backend.models import BaseModel


class User(BaseModel):
    email = Column(String(255), index=True, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(128), server_default='', nullable=False)
    last_name = Column(String(128), server_default='', nullable=False)
    patronymic = Column(String(128), server_default='', nullable=False)
    is_admin = Column(Boolean, server_default=expression.false(), index=True, nullable=False)
    is_teacher = Column(Boolean, server_default=expression.false(), index=True, nullable=False)

    __table_args__ = (
        CheckConstraint('NOT (is_admin AND is_teacher)', name='check_one_role'),
        CheckConstraint("email LIKE '%___@___%.__%'", name='check_email_format'),
    )
