from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.schemas import posts as schemas
from backend.api.queries import posts as queries
from backend.api.queries import subdivisions as subdivisions_queries
from backend.database import get_db
from backend.api.dependencies import ListPageParams
from backend.settings import LimitOffsetPage
from backend.models import Subdivision, Post
from backend.api.errors.errors import not_found
from backend.api.auth import admin_only


router = APIRouter()


def current_subdivision(subdivision_id: int, db: Session = Depends(get_db)):
    subdivision = subdivisions_queries.get_subdivision(db, subdivision_id)
    if subdivision is None:
        raise not_found()
    return subdivision


def current_post(post_id, db: Session = Depends(get_db)):
    post = queries.get_post(db, post_id)
    if post is None:
        raise not_found()
    return post


@router.get('/posts', response_model=LimitOffsetPage[schemas.Post])
def get_posts(
    params: ListPageParams = Depends(),
    db: Session = Depends(get_db),
):
    return queries.get_posts(db, params)


@router.get('/subdivisions/{subdivision_id}/posts', response_model=LimitOffsetPage[schemas.SubdivisionPost])
def get_subdivision_posts(
    params: ListPageParams = Depends(),
    subdivision: Subdivision = Depends(current_subdivision),
    db: Session = Depends(get_db),
):
    return queries.get_posts_by_subdivision_id(db, subdivision.id, params)


@router.get(
    '/subdivisions/{subdivision_id}/posts/{post_id}',
    response_model=schemas.OneSubdivisionPost,
    dependencies=[Depends(current_subdivision)],
)
def get_subdivision_post(post: schemas.OneSubdivisionPost = Depends(current_post)):
    return post


@router.post(
    '/subdivisions/{subdivision_id}/posts',
    response_model=schemas.OneSubdivisionPost,
    dependencies=[Depends(admin_only)],
)
def create_subdivision_post(
    post: schemas.CreateSubdivisionPost,
    subdivision: Subdivision = Depends(current_subdivision),
    db: Session = Depends(get_db),
):
    return queries.create_post(db, post, subdivision_id=subdivision.id)


@router.patch(
    '/subdivisions/{subdivision_id}/posts/{post_id}',
    response_model=schemas.OneSubdivisionPost,
    dependencies=[Depends(current_subdivision), Depends(admin_only)],
)
def update_subdivision_post(
    patch_data: schemas.PatchSubdivisionPost,
    current_post: Post = Depends(current_post),
    db: Session = Depends(get_db),
):
    return queries.update_post(db, current_post, patch_data)


@router.delete(
    '/subdivisions/{subdivision_id}/posts/{post_id}',
    dependencies=[Depends(current_subdivision), Depends(admin_only)],
    status_code=204,
)
def delete_subdivision_post(
    post: Post = Depends(current_post),
    db: Session = Depends(get_db),
):
    queries.delete_post(db, post)
    return {}
