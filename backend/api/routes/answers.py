from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only
from backend.api.current_dependencies import current_task
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found, bad_request
from backend.api.schemas.tasks import Task
from backend.database import get_db
from backend.api.queries import answers as queries
from backend.api.schemas import answers as schemas
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/courses/{course_id}/topics/{topic_id}/tasks/{task_id}/answers')


def current_task_with_predefined_answers(task: Task = Depends(current_task)):
    if not task.task_type.may_have_answers():
        raise bad_request('Unsuitable task type')
    return task


@router.get('/', response_model=LimitOffsetPage[schemas.AnswerAdmin], dependencies=[Depends(admin_only)])
def get_answers(task: Task = Depends(current_task_with_predefined_answers),
                params: ListPageParams = Depends(),
                db: Session = Depends(get_db)):
    return queries.get_answers(db, task.id, params)


@router.get(
    '/{answer_id}',
    response_model=schemas.AnswerAdmin,
    dependencies=[Depends(admin_only), Depends(current_task_with_predefined_answers)],
)
def get_answer(answer_id: int,
               db: Session = Depends(get_db)):
    answer = queries.get_answer(db, answer_id)
    if answer is None:
        raise not_found()
    return answer


@router.post(
    '/',
    response_model=schemas.AnswerAdmin,
    dependencies=[Depends(admin_only)],
)
def create_answer(answer: schemas.CreateAnswer,
                  task: Task = Depends(current_task_with_predefined_answers),
                  db: Session = Depends(get_db)):
    return queries.create_answer(db, answer, task)


@router.delete(
    '/{answer_id}',
    status_code=204,
    dependencies=[Depends(admin_only), Depends(current_task_with_predefined_answers)],
)
def delete_answer(answer_id: int,
                  db: Session = Depends(get_db)):
    answer = queries.get_answer(db, answer_id)
    queries.delete_answer(db, answer)
    return {}


@router.patch(
    '/{answer_id}',
    response_model=schemas.AnswerAdmin,
    dependencies=[Depends(admin_only), Depends(current_task_with_predefined_answers)],
)
def patch_answer(answer_id: int,
                 answer: schemas.PatchAnswer,
                 db: Session = Depends(get_db)):
    answer_to_patch = queries.get_answer(db, answer_id)
    return queries.patch_answer(db, answer_to_patch, answer)
