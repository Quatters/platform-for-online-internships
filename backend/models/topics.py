from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Relationship
from backend.models import BaseModel, Course


class Topic(BaseModel):
    name = Column(String, unique=True, index=True)
    description = Column(String)
    prev_topic_id = Column(Integer, ForeignKey('app_topic.id'), index=True, unique=True)
    #prev_topic = Relationship('app_topic', remote_side='app_topic.id', backref='next_topic')
    course_id = Column(Integer, ForeignKey(Course.id), index=True)
    course = Relationship(Course, primaryjoin=course_id == Course.id)
    __table_args__ = (
            UniqueConstraint(course_id, prev_topic_id, name="u_prev_topic_for_course"),
    )
