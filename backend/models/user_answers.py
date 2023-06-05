from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship, Mapped
from backend.models.base import BaseModel
from backend.models import User, Answer


class UserAnswer(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)
    answer_id = Column(Integer, ForeignKey(Answer.id), nullable=True)
    text_answer = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            'NOT (answer_id IS NULL AND text_answer IS NULL)',
            name='check_answer_is_set',
        ),
    )
