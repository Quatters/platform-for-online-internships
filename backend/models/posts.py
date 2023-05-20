from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel
from backend.models.subdivisions import Subdivision
from backend.models.association_tables import UserPostAssociation


class Post(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)

    subdivision_id = Column(Integer, ForeignKey(Subdivision.id), index=True, nullable=False)
    subdivision = relationship(
        Subdivision,
        primaryjoin=subdivision_id == Subdivision.id,
        back_populates='posts',
    )

    users = relationship('User', secondary=UserPostAssociation, back_populates='posts')
