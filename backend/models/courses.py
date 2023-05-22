from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship, Mapped
from backend.models import BaseModel
from backend.models.association_tables import CoursePostAssociation


class Course(BaseModel):
    name = Column(String(128), index=True, unique=True, nullable=False)
    description = Column(Text, server_default='', nullable=False)

    posts: Mapped[list['Course']] = relationship(
        'Course',
        secondary=CoursePostAssociation,
        back_populates='courses',
    )
