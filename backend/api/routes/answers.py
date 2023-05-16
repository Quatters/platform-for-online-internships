from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.api.auth import get_current_user
from backend.api.errors.errors import not_found, unauthorized
from backend.api.schemas.users import User
from backend.database import get_db
from backend.api.queries import tasks, topics, answers as queries
from backend.api.schemas import answers as schemas


router = APIRouter(prefix='/courses/{course_id}/topics/{topic_id}/tasks/{task_id}/answers')


@router.get('/', response_model=Union[list[schemas.AnswerAdmin], list[schemas.Answer]])
def get_answers(course_id: int,
                topic_id: int,
                task_id: int,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()
    if tasks.get_task(db, task_id) is None:
        raise not_found()
    answers = queries.get_answers(db, task_id)
    if user.is_admin:
        return [schemas.AnswerAdmin.from_orm(answer) for answer in answers]
    return [schemas.Answer.from_orm(answer) for answer in answers]


@router.get('/{answer_id}', response_model=Union[schemas.AnswerAdmin, schemas.Answer])
def get_answer(course_id: int,
               topic_id: int,
               task_id: int,
               answer_id: int,
               user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()
    if tasks.get_task(db, task_id) is None:
        raise not_found()
    answer = queries.get_answer(db, answer_id)
    if answer is None:
        raise not_found()
    if user.is_admin:
        return schemas.AnswerAdmin.from_orm(answer)
    return schemas.Answer.from_orm(answer)


@router.post('/', response_model=schemas.AnswerAdmin)
def create_answer(course_id: int,
                topic_id: int,
                task_id: int,
                answer: schemas.CreateAnswer,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unauthorized()
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()
    if tasks.get_task(db, task_id) is None:
        raise not_found()

    created_task = queries.create_answer(db, answer, task_id)
    return created_task


@router.delete('/{answer_id}', status_code=204)
def delete_answer(course_id: int,
                topic_id: int,
                task_id: int,
                answer_id: int,
                user: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unauthorized()
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()
    if tasks.get_task(db, task_id) is None:
        raise not_found()

    answer = queries.get_answer(db, answer_id)
    queries.delete_answer(db, answer)
    return {}


@router.patch('/{answer_id}', response_model=schemas.AnswerAdmin)
def patch_answer(course_id: int,
               topic_id: int,
               task_id: int,
               answer_id: int,
               answer: schemas.PatchAnswer,
               user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    if not user.is_admin:
        raise unauthorized()
    if topics.get_topic(db, topic_id, course_id) is None:
        raise not_found()
    if tasks.get_task(db, task_id) is None:
        raise not_found()

    answer_to_patch = queries.get_answer(db, answer_id)
    queries.patch_answer(db, answer_to_patch, answer)

    return answer_to_patch
