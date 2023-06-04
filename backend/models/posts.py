from typing import TYPE_CHECKING
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped
from backend.models.base import BaseModel
from backend.models import Subdivision
from backend.models.association_tables import (
    PostCompetenceAssociation,
    UserPostAssociation,
    CoursePostAssociation,
)


if TYPE_CHECKING:  # nocv
    from backend.models import User, Course, Competence


class Post(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)

    subdivision_id = Column(Integer, ForeignKey(Subdivision.id), index=True, nullable=False)
    subdivision: Mapped[Subdivision] = relationship(
        Subdivision,
        primaryjoin=subdivision_id == Subdivision.id,
        back_populates='posts',
    )

    users: Mapped[list['User']] = relationship(
        'User',
        secondary=UserPostAssociation,
        back_populates='posts',
    )
    courses: Mapped[list['Course']] = relationship(
        'Course',
        secondary=CoursePostAssociation,
        back_populates='posts',
    )
    competencies: Mapped[list['Competence']] = relationship(
        'Competence',
        secondary=PostCompetenceAssociation,
        back_populates='posts',
    )
