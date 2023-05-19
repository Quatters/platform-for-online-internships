from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import get_current_user
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found, unauthorized
from backend.api.schemas.users import User
from backend.database import get_db
from backend.api.queries import topics, tasks as queries
from backend.api.schemas import tasks as schemas
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/courses/{course_id}/topics/{topic_id}')


@router.get('/', response_model=LimitOffsetPage[schemas.Task])
def get_tasks(course_id: int,
              topic_id: int,
              params: ListPageParams = Depends(),
              db: Session = Depends(get_db)):
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()
    return queries.get_tasks(db, topic_id, params)


@router.get('/{task_id}', response_model=schemas.OneTask)
def get_task(course_id: int,
             topic_id: int,
             task_id,
             db: Session = Depends(get_db)):
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()
    task = queries.get_task(db, task_id)
    if task is None:
        raise not_found()
    return task


@router.post('/', response_model=schemas.OneTask)
def create_task(course_id: int,
                topic_id: int,
                task: schemas.CreateTask,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unauthorized()
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()

    if task.prev_task_id is not None:
        if queries.get_task(db, task.prev_task_id) is None:
            raise not_found()

    created_task = queries.create_task(db, task, course_id)
    return created_task


@router.delete('/{task_id}', status_code=204)
def delete_task(course_id: int,
                topic_id: int,
                task_id: int,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unauthorized()
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()
    task = queries.get_task(db, task_id)
    if task is None:
        raise not_found()

    queries.delete_task(db, task)
    return {}


@router.patch('/{task_id}', response_model=schemas.OneTask)
def patch_task(course_id: int,
               topic_id: int,
               task_id: int,
               task: schemas.PatchTask,
               user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unauthorized()
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()
    task_to_patch = queries.get_task(db, task_id)
    if task_to_patch is None:
        raise not_found()

    queries.patch_task(db, task_to_patch, task)

    return task_to_patch
