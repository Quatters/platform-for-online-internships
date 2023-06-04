from functools import partial
from sqlalchemy import Column, Table, ForeignKey
from backend.models.base import BaseModel, tablename


def fk(model_name: str):
    return ForeignKey(f'{tablename(model_name)}.id')


PKColumn = partial(Column, primary_key=True, index=True)


UserPostAssociation = Table(
    tablename('user_post_association'),
    BaseModel.metadata,
    PKColumn('user_id', fk('User')),
    PKColumn('post_id', fk('Post')),
)


CoursePostAssociation = Table(
    tablename('course_post_association'),
    BaseModel.metadata,
    PKColumn('course_id', fk('Course')),
    PKColumn('post_id', fk('Post')),
)


CourseCompetenceAssociation = Table(
    tablename('course_competence_association'),
    BaseModel.metadata,
    PKColumn('course_id', fk('Course')),
    PKColumn('post_id', fk('Competence')),
)
