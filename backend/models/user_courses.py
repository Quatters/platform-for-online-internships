from sqlalchemy import Column, Float, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Relationship
from backend.models import BaseModel, Course, User


class UserCourse(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), index=True)
    user = Relationship(User, primaryjoin=user_id == User.id, back_populates='courses')
    course_id = Column(Integer, ForeignKey(Course.id), index=True)
    course = Relationship(Course, primaryjoin=course_id == Course.id, back_populates='users')
    progress = Column(Float, default=0)
    admission_date = Column(DateTime)
    __table_args__ = (
            UniqueConstraint(user_id, course_id, name="u_user_course"),
    )
