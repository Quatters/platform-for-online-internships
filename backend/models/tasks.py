from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import Relationship
from backend.models import BaseModel
from backend.models.task_types import TaskType
from backend.models.topics import Topic


class Task(BaseModel):
    name = Column(String, unique=False, index=True, nullable=False)
    description = Column(String, nullable=False, server_default="")
    task_type = Column(Enum(TaskType), nullable=False, index=True)
    prev_task_id = Column(Integer, ForeignKey('app_task.id'), index=True, unique=True)
    prev_task = Relationship('Task', remote_side=[prev_task_id])
    topic_id = Column(Integer, ForeignKey(Topic.id), index=True, nullable=False)
    topic = Relationship(Topic, primaryjoin=topic_id == Topic.id)

    __table_args__ = (
        UniqueConstraint(topic_id, prev_task_id, name="u_prev_task_for_topic"),
        CheckConstraint('prev_task_id <> id', name='check_prev_task_id_is_not_self'),
    )
