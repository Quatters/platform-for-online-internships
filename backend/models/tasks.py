from typing import TYPE_CHECKING
from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, Relationship, relationship
from backend.models import BaseModel
from backend.models.topics import Topic
from backend.constants import TaskType


if TYPE_CHECKING: # nocv
    from backend.models import Answer


class Task(BaseModel):
    name = Column(String, unique=False, index=True, nullable=False)
    description = Column(String, nullable=False, server_default="")
    task_type = Column(Enum(TaskType), nullable=False, index=True)
    prev_task_id = Column(Integer, ForeignKey('app_task.id'), index=True, unique=True)
    topic_id = Column(Integer, ForeignKey(Topic.id), index=True, nullable=False)

    next_task = Relationship('Task', back_populates='prev_task', uselist=False)
    topic = Relationship(Topic, primaryjoin=topic_id == Topic.id, back_populates='tasks')

    answers: Mapped[list['Answer']] = relationship('Answer', cascade="all, delete")

    __table_args__ = (
        UniqueConstraint(topic_id, prev_task_id, name="u_prev_task_for_topic"),
        CheckConstraint('prev_task_id <> id', name='check_prev_task_id_is_not_self'),
    )


Task.prev_task = Relationship(Task, remote_side=[Task.id], uselist=False)
