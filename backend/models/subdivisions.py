from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel


class Subdivision(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)

    posts = relationship('Post')
