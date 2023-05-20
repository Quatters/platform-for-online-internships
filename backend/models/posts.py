from typing import TYPE_CHECKING
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped
from backend.models.base import BaseModel
from backend.models import Subdivision
from backend.models.association_tables import UserPostAssociation


if TYPE_CHECKING:
    from backend.models import User


class Post(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)

    subdivision_id = Column(Integer, ForeignKey(Subdivision.id), index=True, nullable=False)
    subdivision: Mapped[Subdivision] = relationship(
        Subdivision,
        primaryjoin=subdivision_id == Subdivision.id,
        back_populates='posts',
    )

    users: Mapped[list['User']] = relationship('User', secondary=UserPostAssociation, back_populates='posts')
