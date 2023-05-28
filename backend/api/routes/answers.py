from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import admin_only, get_current_user
from backend.api.current_dependencies import current_task
from backend.api.dependencies import ListPageParams
from backend.api.errors.errors import not_found, unauthorized, bad_request
from backend.api.schemas.tasks import Task
from backend.api.schemas.users import User
from backend.database import get_db
from backend.api.queries import answers as queries
from backend.api.schemas import answers as schemas
from backend.settings import LimitOffsetPage


router = APIRouter(prefix='/courses/{course_id}/topics/{topic_id}/tasks/{task_id}/answers')


@router.get('/',
            response_model=LimitOffsetPage[schemas.AnswerAdmin | schemas.Answer])
def get_answers(task: Task = Depends(current_task),
                user: User = Depends(get_current_user),
                params: ListPageParams = Depends(),
                db: Session = Depends(get_db)):
    if not task.task_type.may_have_answers():
        raise bad_request('Unsuitable task type')

    answers = queries.get_answers(db, task.id, params)
    if not user.is_admin:
        for item in answers.items:
            del item.is_correct
    return answers


@router.get('/{answer_id}', response_model=schemas.AnswerAdmin | schemas.Answer)
def get_answer(answer_id: int,
               task: Task = Depends(current_task),
               user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    if not task.task_type.may_have_answers():
        raise bad_request('Unsuitable task type')
    answer = queries.get_answer(db, answer_id)
    if answer is None:
        raise not_found()
    if user.is_admin:
        return schemas.AnswerAdmin.from_orm(answer)
    return schemas.Answer.from_orm(answer)


@router.post(
    '/',
    response_model=schemas.AnswerAdmin,
    dependencies=[Depends(admin_only)],
)
def create_answer(answer: schemas.CreateAnswer,
                  task: Task = Depends(current_task),
                  db: Session = Depends(get_db)):
    if not task.task_type.may_have_answers():
        raise bad_request('Unsuitable task type')

    created_task = queries.create_answer(db, answer, task.id)
    return created_task


@router.delete(
    '/{answer_id}',
    status_code=204,
    dependencies=[Depends(admin_only), Depends(current_task)],
)
def delete_answer(answer_id: int,
                  db: Session = Depends(get_db)):
    answer = queries.get_answer(db, answer_id)
    queries.delete_answer(db, answer)
    return {}


@router.patch(
    '/{answer_id}',
    response_model=schemas.AnswerAdmin,
    dependencies=[Depends(admin_only)],
)
def patch_answer(answer_id: int,
                 answer: schemas.PatchAnswer,
                 task: Task = Depends(current_task),
                 db: Session = Depends(get_db)):
    if not task.task_type.may_have_answers():
        raise bad_request('Unsuitable task type')

    answer_to_patch = queries.get_answer(db, answer_id)
    queries.patch_answer(db, answer_to_patch, answer)

    return answer_to_patch
