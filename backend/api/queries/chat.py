import sqlalchemy as sa
from sqlalchemy.orm import Session, joinedload
from fastapi_pagination.ext.sqlalchemy import paginate
from backend.models import ChatMessage, User
from backend.api.dependencies import LimitOffsetParams


def get_messages(db: Session, sender: User, recipient: User, params: LimitOffsetParams):
    query = db.query(
        ChatMessage,
    ).where(
        (ChatMessage.sender_id == sender.id) & (ChatMessage.recipient_id == recipient.id)
        | (ChatMessage.sender_id == recipient.id) & (ChatMessage.recipient_id == sender.id)
    ).options(
        joinedload(ChatMessage.sender, innerjoin=True),
        joinedload(ChatMessage.recipient, innerjoin=True),
    ).order_by(
        ChatMessage.created_at.desc(),
    )
    return paginate(query, params)


def create_message(db: Session, sender: User, recipient: User, message: str):
    message = ChatMessage(
        sender=sender,
        recipient=recipient,
        message=message,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def users_can_chat(db: Session, teacher: User, intern: User):
    return db.scalar(
        sa.select(
            sa.exists(
                sa.select(
                    User.id
                ).where(
                    User.teacher_id == teacher.id, User.id == intern.id
                )
            )
        )
    )
