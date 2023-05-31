from fastapi_pagination import paginate as pypaginate
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.models.tasks import Task
from backend.api.schemas import tasks as schemas
from backend.api.queries.helpers import sort_by_self_fk, with_search


def get_tasks(db: Session, topic_id: int, params: ListPageParams):
    query = db.query(Task).filter(Task.topic_id == topic_id)
    query = with_search(Task.name, query=query, search=params.search)

    tasks = sort_by_self_fk(query, 'prev_task_id')
    return pypaginate(
        tasks,
        params,
        length_function=lambda _: query.count(),
    )


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
