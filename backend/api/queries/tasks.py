from typing import List
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.models.tasks import Task
from backend.api.schemas import tasks as schemas


def get_tasks(db: Session, topic_id: int, params: ListPageParams) -> List[Task]:
    query = db.query(Task).filter(Task.topic_id == topic_id)
    if s := params.search:
        query = query.filter(func.lower(Task.name).like(f'%{s.lower()}%'))
    vals = paginate(query, params)

    firsts = [item for item in vals.items if item.prev_task_id is None]
    cur = firsts[0]

    result = [cur]
    vals.items.remove(cur)
    while len(vals.items) > 0:
        for obj in vals.items:
            if obj.prev_task_id == cur.id:
                cur = obj
                result.append(cur)
                vals.items.remove(obj)

    vals.items = result
    return vals


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).get(task_id)


def get_next_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.prev_task_id == task_id).one_or_none()


def create_task(db: Session, topic: schemas.CreateTask, topic_id: int) -> Task:
    topic = Task(**topic.dict())
    topic.topic_id = topic_id
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()


def patch_task(db: Session, task: Task, data: schemas.PatchTask) -> Task:
    db.query(Task).filter(Task.id == task.id).update(data.dict(exclude_unset=True))
    db.commit()
    db.refresh(task)
    return task
