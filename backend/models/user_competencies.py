from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from backend.models.base import BaseModel
from backend.models import User, Competence


class UserCompetence(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False, index=True)
    competence_id = Column(Integer, ForeignKey(Competence.id), nullable=False, index=True)

    user: Mapped[User] = relationship(User, primaryjoin=user_id == User.id, back_populates='competencies')
