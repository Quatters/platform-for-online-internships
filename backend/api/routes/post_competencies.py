from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only
from backend.api.current_dependencies import current_post
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found
from backend.database import get_db
from backend.api.queries import post_competencies as queries
from backend.api.queries import competencies as queries_competencies
from backend.api.schemas import post_competencies as schemas
from backend.models.post_competencies import PostCompetence
from backend.models.posts import Post
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/subdivisions/{subdivision_id}/posts/{post_id}/competencies')


async def get_current_post_competence(post_competence_id: int,
                                      post: Post = Depends(current_post),
                                      db: Session = Depends(get_db)) -> PostCompetence:
    post_competence = queries.get_post_competence(db, post_competence_id)
    if post_competence is None:
        raise not_found()
    if post_competence.post_id != post.id:
        raise not_found()
    return post_competence


@router.get('/', response_model=LimitOffsetPage[schemas.PostCompetence])
def get_post_competencies(post: Post = Depends(current_post),
                            params: ListPageParams = Depends(),
                            db: Session = Depends(get_db)):
    return queries.get_post_competencies(db, params, post.id)


@router.post('/', response_model=schemas.PostCompetence, dependencies=[Depends(admin_only)])
def create_competence(post_competence: schemas.CreatePostCompetence,
                      post: Post = Depends(current_post),
                      db: Session = Depends(get_db)):
    competence = queries_competencies.get_competence(db, post_competence.competence_id)
    if competence is None:
        raise not_found()
    created = queries.create_post_competence(db, post_competence, post.id)
    created.post_name = created.post.name
    created.competence_name = created.competence.name
    return created


@router.delete('/{post_competence_id}', status_code=204, dependencies=[Depends(admin_only)])
def delete_compentence(post_competence: PostCompetence = Depends(get_current_post_competence),
                       db: Session = Depends(get_db)):
    queries.delete_post_competence(db, post_competence)
    return {}
