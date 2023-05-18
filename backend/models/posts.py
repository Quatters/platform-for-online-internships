from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import Relationship
from backend.models.base import BaseModel
from backend.models.subdivisions import Subdivision


class Post(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)
    subdivision_id = Column(Integer, ForeignKey(Subdivision.id), index=True)
    subdivision = Relationship(Subdivision, primaryjoin=subdivision_id == Subdivision.id)
