from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from backend.api.current_dependencies import current_post, current_subdivision
from backend.api.schemas import posts as schemas
from backend.api.queries import posts as queries
from backend.database import get_db
from backend.api.dependencies import ListPageParams, PostsListPageParams
from backend.settings import LimitOffsetPage
from backend.models import Subdivision, Post
from backend.api.auth import admin_only
from backend.api.background_tasks.users import handle_user_teachers_after_post_change


router = APIRouter()


@router.get('/posts', response_model=LimitOffsetPage[schemas.Post])
def get_posts(
    params: PostsListPageParams = Depends(),
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


@router.post(
    '/posts',
    response_model=schemas.Post,
    dependencies=[Depends(admin_only)],
)
def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(get_db),
):
    subdivision_post = schemas.CreateSubdivisionPost(**post.dict())
    return queries.create_post(db, subdivision_post, subdivision_id=post.subdivision_id)


@router.patch(
    '/subdivisions/{subdivision_id}/posts/{post_id}',
    response_model=schemas.OneSubdivisionPost,
    dependencies=[Depends(current_subdivision), Depends(admin_only)],
)
def update_subdivision_post(
    patch_data: schemas.PatchSubdivisionPost,
    current_post: schemas.OneSubdivisionPost = Depends(current_post),
    db: Session = Depends(get_db),
):
    return queries.update_post(db, current_post, patch_data)


@router.delete(
    '/subdivisions/{subdivision_id}/posts/{post_id}',
    dependencies=[Depends(current_subdivision), Depends(admin_only)],
    status_code=204,
)
def delete_subdivision_post(
    background_tasks: BackgroundTasks,
    post: Post = Depends(current_post),
    db: Session = Depends(get_db),
):
    queries.delete_post(db, post)
    background_tasks.add_task(handle_user_teachers_after_post_change, db)
    return {}
