from sqlalchemy import Column, String, Text
from backend.models import BaseModel


class Course(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)
