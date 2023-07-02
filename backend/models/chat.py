import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel
from backend.models import User


class ChatMessage(BaseModel):
    sender_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False)
    recipient_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now(), nullable=False)
    message = sa.Column(sa.Text, nullable=False)

    sender = relationship(User, foreign_keys=sender_id)
    recipient = relationship(User, foreign_keys=recipient_id)

    __table_args__ = (
        sa.Index('idx_sender_recipient_created_at', sender_id, recipient_id, created_at.desc(), unique=True),
        sa.CheckConstraint('sender_id <> recipient_id', name='check_sender_and_recipient_not_equal'),
    )
