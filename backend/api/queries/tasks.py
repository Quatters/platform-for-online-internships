from functools import partial
from fastapi_pagination import paginate as pypaginate
from sqlalchemy.orm import Session
from backend.api.dependencies import ListPageParams
from backend.models.tasks import Task
from backend.api.schemas import tasks as schemas
from backend.api.queries.helpers import (
    create_with_respect_to_prev_instance,
    update_with_respect_to_prev_instance,
    delete_with_respect_to_prev_instance,
    sort_by_self_fk,
    with_search,
)


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
    return db.get(Task, task_id)


def get_first_task(db: Session, topic_id: int):
    return db.query(Task).filter(
        (Task.topic_id == topic_id) & (Task.prev_task_id == None)  # noqa: E711
    ).one_or_none()


def create_task(db: Session, task: schemas.CreateTask, topic_id: int) -> Task:
    return create_with_respect_to_prev_instance(
        db=db,
        create_data={**task.dict(), 'topic_id': topic_id},
        model=Task,
        prev_id_attr_name='prev_task_id',
        next_instance_attr_name='next_task',
        get_first_func=partial(get_first_task, db, topic_id),
        get_prev_func=partial(get_task, db, task.prev_task_id),
    )


def delete_task(db: Session, task: Task):
    delete_with_respect_to_prev_instance(
        db=db,
        instance=task,
        prev_id_attr_name='prev_task_id',
        next_instance_attr_name='next_task',
    )


def patch_task(db: Session, task: Task, data: schemas.PatchTask) -> Task:
    return update_with_respect_to_prev_instance(
        db=db,
        instance=task,
        prev_id_attr_name='prev_task_id',
        next_instance_attr_name='next_task',
        update_data=data.dict(exclude_unset=True),
        additional_filters_to_search_for_instance_to_update=[
            Task.topic_id == task.topic_id,
        ]
    )
