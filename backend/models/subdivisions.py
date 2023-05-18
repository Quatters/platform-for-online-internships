from sqlalchemy import Column, String, Text
from backend.models.base import BaseModel


class Subdivision(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)
