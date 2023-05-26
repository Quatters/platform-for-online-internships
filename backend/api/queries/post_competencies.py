from fastapi_pagination import paginate
from sqlalchemy.orm import Session, joinedload
from backend.api.dependencies import ListPageParams
from backend.api.schemas import post_competencies as schemas
from backend.models.competencies import Competence as CompetenceModel
from backend.models.posts import Post as PostModel
from backend.models.post_competencies import PostCompetence


def get_post_competencies(db: Session, params: ListPageParams, post_id: int):
    query = db.query(PostCompetence) \
              .filter(PostCompetence.post_id == post_id) \
              .options(
                joinedload(PostCompetence.post, innerjoin=True).load_only(PostModel.name),
                joinedload(PostCompetence.competence, innerjoin=True).load_only(CompetenceModel.name)
              )
    objects = query \
            .limit(params.limit) \
            .offset(params.offset) \
            .all()
    for obj in objects:
        obj.post_name = obj.post.name
        obj.competence_name = obj.competence.name

    return paginate(objects, params, length_function=lambda _: query.count())


def get_post_competence(db: Session, post_competence_id: int):
    return db.query(PostCompetence).get(post_competence_id)


def create_post_competence(db: Session, post_competence: schemas.CreatePostCompetence, post_id: int):
    post_competence = PostCompetence(**post_competence.dict())
    post_competence.post_id = post_id
    db.add(post_competence)
    db.commit()
    db.refresh(post_competence)
    return post_competence


def delete_post_competence(db: Session, competence: PostCompetence):
    db.delete(competence)
    db.commit()

