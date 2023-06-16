import orjson
from sqlalchemy import Column, ForeignKey, Integer, Text, Enum, String
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM
from sqlalchemy.orm import relationship, Mapped
from backend.models.base import BaseModel
from backend.models import User, TestAttempt
from backend.constants import UserAnswerStatus, TaskType


class UserAnswer(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)
    _value = Column(Text, nullable=False)
    attempt_id = Column(Integer, ForeignKey(TestAttempt.id), nullable=False)
    status = Column(Enum(UserAnswerStatus), nullable=False, index=True)
    task_name = Column(String, nullable=False)
    task_description = Column(String, nullable=False)
    task_type = Column(PG_ENUM(TaskType, create_type=False), nullable=False)
    score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    review = Column(Text)

    attempt: Mapped[TestAttempt] = relationship(foreign_keys=attempt_id, back_populates='user_answers')

    @property
    def value(self) -> str | list[str]:
        if self.task_type is TaskType.multiple:
            return orjson.loads(self._value)
        return self._value

    @value.setter
    def value(self, new_value: str | list[str]):
        if isinstance(new_value, list):
            self._value = orjson.dumps(new_value).decode()
        else:
            self._value = new_value
