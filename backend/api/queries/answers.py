from typing import List
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.api.schemas import answers as schemas
from backend.models.answers import Answer
from backend.constants import TaskType


def get_answers(db: Session, task_id: int, params: ListPageParams) -> List[Answer]:
    query = db.query(Answer).filter(Answer.task_id == task_id)
    return paginate(query, params)


def get_answer(db: Session, answer_id) -> Answer | None:
    return db.get(Answer, answer_id)


def create_answer(db: Session, answer: schemas.CreateAnswer, task_id: int) -> Answer:
    answer = Answer(**answer.dict())
    answer.task_id = task_id
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def delete_answer(db: Session, answer: Answer):
    db.delete(answer)
    db.commit()


def patch_answer(db: Session, answer: Answer, data: schemas.PatchAnswer) -> Answer:
    if answer.task.task_type is TaskType.single and data.is_correct:
        another_correct_answer = db.query(Answer).filter(Answer.is_correct).one_or_none()
        if another_correct_answer is not None:
            another_correct_answer.is_correct = False
    db.query(Answer).filter(Answer.id == answer.id).update(data.dict(exclude_unset=True))
    db.commit()
    db.refresh(answer)
    return answer
