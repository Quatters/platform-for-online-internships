from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import Relationship
from backend.models import BaseModel, Course


class Topic(BaseModel):
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False, server_default="")
    prev_topic_id = Column(Integer, ForeignKey('app_topic.id'), index=True, unique=True)
    course_id = Column(Integer, ForeignKey(Course.id), index=True, nullable=False)
    course = Relationship(Course, primaryjoin=course_id == Course.id)

    __table_args__ = (
        UniqueConstraint(course_id, prev_topic_id, name="u_prev_topic_for_course"),
        CheckConstraint('prev_topic_id <> id', name='check_prev_topic_id_is_not_self')
    )

Topic.prev_topic = Relationship(Topic, remote_side=[Topic.id], uselist=False)
