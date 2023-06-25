from typing import List
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.api.schemas import answers as schemas
from backend.models import Answer, Task
from backend.constants import TaskType


def get_answers(db: Session, task_id: int, params: ListPageParams) -> List[Answer]:
    query = db.query(Answer).filter(Answer.task_id == task_id)
    return paginate(query, params)


def get_answer(db: Session, answer_id) -> Answer | None:
    return db.get(Answer, answer_id)


def _handle_single_correct_answer(db: Session, task_id: int):
    db.query(Answer).filter(
        Answer.task_id == task_id,
        Answer.is_correct,
    ).update({
        Answer.is_correct: False,
    })


def create_answer(db: Session, answer: schemas.CreateAnswer, task: Task) -> Answer:
    answer = Answer(**answer.dict())
    answer.task = task
    if task.task_type is TaskType.single and answer.is_correct:
        _handle_single_correct_answer(db, task.id)
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def delete_answer(db: Session, answer: Answer):
    db.delete(answer)
    db.commit()


def patch_answer(db: Session, answer: Answer, data: schemas.PatchAnswer) -> Answer:
    if answer.task.task_type is TaskType.single and data.is_correct:
        _handle_single_correct_answer(db, answer.task_id)
    db.query(Answer).filter(Answer.id == answer.id).update(data.dict(exclude_unset=True))
    db.commit()
    db.refresh(answer)
    return answer
