from typing import TYPE_CHECKING
from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, relationship
from backend.models import BaseModel
from backend.models.association_tables import CourseCompetenceAssociation


if TYPE_CHECKING:
    from backend.models import Course


class Competence(BaseModel):
    name = Column(String, nullable=False, unique=True, index=True)

    courses: Mapped[list['Course']] = relationship(
        'Course',
        secondary=CourseCompetenceAssociation,
        back_populates='competencies',
    )
