from sqlalchemy.orm import Session
from backend.models.users import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter_by(email=email).first()
