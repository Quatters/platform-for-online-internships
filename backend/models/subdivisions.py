from typing import TYPE_CHECKING
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship, Mapped
from backend.models.base import BaseModel


if TYPE_CHECKING:  # nocv
    from backend.models import Post


class Subdivision(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)

    posts: Mapped[list['Post']] = relationship('Post', cascade="all, delete")
