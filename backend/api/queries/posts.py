from sqlalchemy.orm import Session, load_only
from fastapi_pagination.ext.sqlalchemy import paginate
from backend.api.dependencies import ListPageParams
from backend.models import Post
from backend.api.schemas import posts as schemas
from backend.api.queries.helpers import with_search


def get_post_by_subdivision_id(db: Session, subdivision_id: int, params: ListPageParams):
    query = db.query(Post).filter(Post.subdivision_id == subdivision_id).options(load_only(
        Post.id,
        Post.name,
    ))
    query = with_search(Post.name, query=query, search=params.search)
    return paginate(query)


def get_post(db: Session, post_id):
    return db.query(Post).get(post_id)


def create_post(db: Session, post: Post, subdivision_id: int):
    post = Post(subdivision_id=subdivision_id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: Post):
    db.delete(post)
    db.commit()


def update_post(db: Session, post: Post, patch_data: schemas.PatchPost):
    db.query(Post).filter(Post.id == post.id).update(patch_data.dict(exclude_unset=True))
    db.commit()
    db.refresh(post)
    return post
