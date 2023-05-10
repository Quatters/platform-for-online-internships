from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Relationship
from backend.models import BaseModel, Course


class Topic(BaseModel):
    name = Column(String, unique=True, index=True)
    description = Column(String)
    index = Column(Integer, index=True)
    course_id = Column(Integer, ForeignKey(Course.id), index=True)
    course = Relationship(Course, primaryjoin=course_id == Course.id)
    __table_ars__ = (
        UniqueConstraint(index, course_id, name='u_course_index'),
    )
