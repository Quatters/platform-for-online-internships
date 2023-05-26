from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Relationship
from backend.models import BaseModel
from backend.models.competencies import Competence
from backend.models.posts import Post


class PostCompetence(BaseModel):
    post_id = Column(Integer, ForeignKey(Post.id), index=True, nullable=False)
    post = Relationship(Post, primaryjoin=post_id == Post.id)
    competence_id = Column(Integer, ForeignKey(Competence.id), index=True, nullable=False)
    competence = Relationship(Competence, primaryjoin=competence_id == Competence.id)
    __table_args__ = (
            UniqueConstraint(post_id, competence_id, name='u_post_competence'),
    )

