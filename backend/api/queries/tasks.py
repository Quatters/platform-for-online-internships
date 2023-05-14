from typing import List
from sqlalchemy.orm import Session
from backend.models.tasks import Task
from backend.api.schemas import tasks as schemas

def get_tasks(db: Session, topic_id: int) -> List[Task]:
    return db.query(Task).filter(Task.topic_id == topic_id).all()


def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).get(task_id)


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
