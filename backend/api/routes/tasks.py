from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.current_dependencies import current_task, current_topic
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found
from backend.api.schemas.topics import Topic
from backend.database import get_db
from backend.api.queries import tasks as queries
from backend.api.schemas import tasks as schemas
from backend.models.tasks import Task
from backend.settings import LimitOffsetPage
from backend.api.auth import admin_only


router = APIRouter(prefix='/courses/{course_id}/topics/{topic_id}/tasks')


@router.get('/', response_model=LimitOffsetPage[schemas.Task])
def get_tasks(topic: Topic = Depends(current_topic),
              params: ListPageParams = Depends(),
              db: Session = Depends(get_db)):
    return queries.get_tasks(db, topic.id, params)


@router.get('/{task_id}', response_model=schemas.OneTask)
def get_task(task: Task = Depends(current_task)):
    return task


@router.post('/', response_model=schemas.OneTask, dependencies=[Depends(admin_only)])
def create_task(task: schemas.CreateTask,
                topic: Topic = Depends(current_topic),
                db: Session = Depends(get_db)):
    if task.prev_task_id is not None:
        if queries.get_task(db, task.prev_task_id) is None:
            raise not_found()

    return queries.create_task(db, task, topic.id)


@router.delete('/{task_id}', status_code=204, dependencies=[Depends(admin_only)])
def delete_task(task: Task = Depends(current_task),
                db: Session = Depends(get_db)):
    queries.delete_task(db, task)
    return {}


@router.patch(
    '/{task_id}',
    response_model=schemas.OneTask,
    dependencies=[Depends(admin_only)],
)
def patch_task(task: schemas.PatchTask,
               task_to_patch: Task = Depends(current_task),
               db: Session = Depends(get_db)):
    return queries.patch_task(db, task_to_patch, task)
