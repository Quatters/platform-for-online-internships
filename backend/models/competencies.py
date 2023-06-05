from typing import TYPE_CHECKING
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship
from backend.models import BaseModel
from backend.models.association_tables import CourseCompetenceAssociation, PostCompetenceAssociation


if TYPE_CHECKING:  # nocv
    from backend.models import Course, Post


class Competence(BaseModel):
    name = Column(String, nullable=False, unique=True, index=True)

    courses: Mapped[list['Course']] = relationship(
        'Course',
        secondary=CourseCompetenceAssociation,
        back_populates='competencies',
    )
    posts: Mapped[list['Post']] = relationship(
        'Post',
        secondary=PostCompetenceAssociation,
        back_populates='competencies',
    )
