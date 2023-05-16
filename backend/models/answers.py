from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Relationship
from backend.models import BaseModel
from backend.models.tasks import Task


class Answer(BaseModel):
    value = Column(String)
    task_id = Column(Integer, ForeignKey(Task.id), index=True)
    task = Relationship(Task, primaryjoin=task_id == Task.id)
    is_correct = Column(Boolean)
    __table_args__ = (
            UniqueConstraint(task_id, value, name="u_answer_value_for_task"),
    )
