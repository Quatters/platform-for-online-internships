from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func
from backend.models import BaseModel, Topic, User


class TestAttempt(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), index=True, nullable=False)
    topic_id = Column(Integer, ForeignKey(Topic.id), index=True, nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_to_pass = Column(Integer, nullable=False)  # seconds
    ended_at = Column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(
        User,
        primaryjoin=user_id == User.id,
        back_populates='test_attempts',
    )
    topic: Mapped[Topic] = relationship(
        Topic,
        primaryjoin=topic_id == Topic.id,
    )
