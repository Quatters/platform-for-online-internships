from sqlalchemy import Column, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Relationship
from backend.models import BaseModel, Course, User


class UserCourse(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), index=True)
    user = Relationship(User, primaryjoin=user_id==User.id)
    course_id = Column(Integer, ForeignKey(Course.id), index=True)
    course = Relationship(Course, primaryjoin=course_id==Course.id)
    progress = Column(Float, nullable=True)
    admission_date = Column(DateTime, nullable=True)
