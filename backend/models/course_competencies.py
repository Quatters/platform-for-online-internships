from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Relationship
from backend.models import BaseModel
from backend.models.competencies import Competence
from backend.models.courses import Course


class CourseCompetence(BaseModel):
    course_id = Column(Integer, ForeignKey(Course.id), index=True, nullable=False)
    course = Relationship(Course, primaryjoin=course_id == Course.id)
    competence_id = Column(Integer, ForeignKey(Competence.id), index=True, nullable=False)
    competence = Relationship(Competence, primaryjoin=competence_id == Competence.id)
    __table_args__ = (
            UniqueConstraint(course_id, competence_id, name='u_course_competence'),
    )
