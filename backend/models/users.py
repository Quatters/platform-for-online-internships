from typing import TYPE_CHECKING
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, CheckConstraint
from sqlalchemy.sql import expression
from sqlalchemy.orm import relationship, Mapped
from backend.models import BaseModel
from backend.models.association_tables import UserPostAssociation


if TYPE_CHECKING:  # nocv
    from backend.models import Post, TestAttempt, UserCompetence, UserCourse


class User(BaseModel):
    email = Column(String(255), index=True, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(128), server_default='', nullable=False)
    last_name = Column(String(128), server_default='', nullable=False)
    patronymic = Column(String(128), server_default='', nullable=False)
    is_admin = Column(Boolean, server_default=expression.false(), index=True, nullable=False)
    is_teacher = Column(Boolean, server_default=expression.false(), index=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey('app_user.id'))

    posts: Mapped[list['Post']] = relationship('Post', secondary=UserPostAssociation, back_populates='users')
    test_attempts: Mapped[list['TestAttempt']] = relationship('TestAttempt', back_populates='user')
    competencies: Mapped[list['UserCompetence']] = relationship('UserCompetence', back_populates='user')
    courses: Mapped[list['UserCourse']] = relationship('UserCourse', cascade='all, delete')
    teacher: Mapped['User'] = relationship(
        primaryjoin='~(User.is_admin | User.is_teacher) & (User.teacher_id == remote(User.id))'
    )
    interns: Mapped[list['User']] = relationship(
        primaryjoin='(User.is_teacher) & (remote(User.teacher_id) == User.id)'
    )

    __table_args__ = (
        CheckConstraint('NOT (is_admin AND is_teacher)', name='check_one_role'),
        CheckConstraint("email LIKE '%___@___%.__%'", name='check_email_format'),
    )
