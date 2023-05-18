from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import get_current_user
from backend.api.errors.errors import not_found, unauthorized
from backend.api.schemas import subdivisions as schemas
from backend.api.queries import subdivisions as queries
from backend.api.dependencies import ListPageParams
from backend.api.schemas.users import User
from backend.settings import LimitOffsetPage
from backend.database import get_db


router = APIRouter(prefix='/subdivisions')


@router.get('/', response_model=LimitOffsetPage[schemas.Subdivision])
def get_subdivisions(params: ListPageParams = Depends(), db: Session = Depends(get_db),):
    return queries.get_subdivisions(db, params)


@router.get('/{subdivision_id}', response_model=schemas.OneSubdivision)
def get_one_subdivision(subdivision_id: int, db: Session = Depends(get_db)):
    subdivision = queries.get_subdivision(db, subdivision_id)
    if subdivision is None:
        raise not_found()
    return subdivision


@router.post('/', response_model=schemas.OneSubdivision)
def create_subdivision(
    subdivision: schemas.CreateSubdivision,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user.is_admin:
        raise unauthorized()
    return queries.create_subdivision(db, subdivision)


@router.delete('/{subdivision_id}', status_code=204)
def delete_subdivision(
    course_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user.is_admin:
        raise unauthorized()
    subdivision = queries.get_subdivision(db, course_id)
    if subdivision is None:
        raise not_found()
    queries.delete_subdivision(db, subdivision)
    return {}


@router.patch('/{course_id}', response_model=schemas.OneSubdivision)
def patch_course(
    course_id: int,
    subdivision: schemas.PatchSubdivision,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user.is_admin:
        raise unauthorized()
    subdivision_to_patch = queries.get_course(db, course_id)
    if subdivision_to_patch is None:
        raise not_found()
    return queries.update_subdivision(db, subdivision_to_patch, subdivision)
