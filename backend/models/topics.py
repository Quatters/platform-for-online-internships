from typing import TYPE_CHECKING
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    CheckConstraint,
    Enum,
    Text,
)
from sqlalchemy.orm import Relationship, relationship, Mapped
from sqlalchemy.sql import text
from backend.models import BaseModel, Course
from backend.constants import TopicResourceType


if TYPE_CHECKING:  # nocv
    from backend.models import Task


class Topic(BaseModel):
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False, server_default="")
    prev_topic_id = Column(Integer, ForeignKey('app_topic.id'), index=True, unique=True)
    course_id = Column(Integer, ForeignKey(Course.id), index=True, nullable=False)
    attempts_amount = Column(Integer, nullable=False, server_default=text('3'))

    next_topic = Relationship('Topic', back_populates='prev_topic', uselist=False)
    course = Relationship(Course, primaryjoin=course_id == Course.id, back_populates='topics')
    tasks: Mapped[list['Task']] = relationship('Task', cascade="all, delete")

    __table_args__ = (
        UniqueConstraint(course_id, prev_topic_id, name="u_prev_topic_for_course"),
        CheckConstraint('prev_topic_id <> id', name='check_prev_topic_id_is_not_self')
    )


Topic.prev_topic = Relationship(Topic, remote_side=[Topic.id], uselist=False)


class TopicResource(BaseModel):
    type = Column(Enum(TopicResourceType), nullable=False, index=True)
    name = Column(String, nullable=False)
    value = Column(Text, nullable=False)
    prev_resource_id = Column(Integer, ForeignKey('app_topicresource.id'), index=True)
    topic_id = Column(Integer, ForeignKey(Topic.id), index=True, nullable=False)

    topic = Relationship(Topic, primaryjoin=topic_id == Topic.id)
    next_resource = Relationship('TopicResource', back_populates='prev_resource', uselist=False)

    __table_args__ = (
        UniqueConstraint(topic_id, prev_resource_id, name='u_prev_resource_per_topic'),
        CheckConstraint('prev_resource_id <> id', name='check_prev_resource_id_is_not_self'),
    )


TopicResource.prev_resource = Relationship(TopicResource, remote_side=[TopicResource.id], uselist=False)
