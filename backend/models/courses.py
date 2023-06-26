from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, Column, Integer, String, Text, text
from sqlalchemy.orm import relationship, Mapped
from backend.models import BaseModel
from backend.models.association_tables import CourseCompetenceAssociation, CoursePostAssociation


if TYPE_CHECKING:  # nocv
    from backend.models import Post
    from backend.models import Competence
    from backend.models import Topic
    from backend.models import UserCourse


class Course(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)
    pass_percent = Column(Integer, server_default=text('86'), nullable=False)

    topics: Mapped[list['Topic']] = relationship('Topic', cascade="all, delete")
    users: Mapped[list['UserCourse']] = relationship('UserCourse', cascade='all, delete')

    posts: Mapped[list['Post']] = relationship(
        'Post',
        secondary=CoursePostAssociation,
        back_populates='courses',
    )
    competencies: Mapped[list['Competence']] = relationship(
        'Competence',
        secondary=CourseCompetenceAssociation,
        back_populates='courses',
    )

    __table_args__ = (
        CheckConstraint(
            'pass_percent >= 1 AND pass_percent <= 100',
            name='check_pass_percent_between_1_and_100',
        ),
    )
