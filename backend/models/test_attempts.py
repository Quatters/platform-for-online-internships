from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, DateTime, Enum
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func, text
from backend.models import BaseModel, Topic, User, UserCourse
from backend.constants import TestAttemptStatus


if TYPE_CHECKING:  # nocv
    from backend.models import UserAnswer


class TestAttempt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    topic_id = Column(Integer, ForeignKey(Topic.id), index=True, nullable=False)
    user_course_id = Column(Integer, ForeignKey(UserCourse.id, ondelete='SET NULL'), index=True, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_to_pass = Column(Integer, nullable=False)  # seconds
    finished_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(Enum(TestAttemptStatus), nullable=False, index=True)
    score = Column(Integer, server_default=text('0'), nullable=False)
    max_score = Column(Integer, server_default=text('0'), nullable=False)

    user: Mapped[User] = relationship(
        User,
        primaryjoin=user_id == User.id,
        back_populates='test_attempts',
    )
    topic: Mapped[Topic] = relationship(
        Topic,
        primaryjoin=topic_id == Topic.id,
    )
    user_course: Mapped[UserCourse] = relationship(
        UserCourse,
        primaryjoin=user_course_id == UserCourse.id,
        passive_deletes=True,
    )
    user_answers: Mapped[list['UserAnswer']] = relationship(back_populates='attempt')

    __test__ = False
