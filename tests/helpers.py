from datetime import datetime
from typing import Optional
from uuid import uuid1
from httpx import Client
from sqlalchemy import Column
from sqlalchemy.orm import Session
from backend.models import (
    Course,
    Competence,
    Topic,
    TopicResource,
    Subdivision,
    Post,
    Task,
    User,
    UserCourse,
    Answer,
)
from backend.constants import TaskType, TopicResourceType
from backend.api.utils import hash_password
from tests.base import login_as, test_admin


def create_user(
    db: Session,
    *,
    first_name: str | None = None,
    last_name: str | None = None,
    patronymic: str | None = None,
    email: str | None = None,
    password: str = 'test',
    is_admin: bool = False,
    is_teacher: bool = False,
    commit: bool = True,
):
    user = User(
        first_name=first_name or str(uuid1()),
        last_name=last_name or str(uuid1()),
        patronymic=patronymic or str(uuid1()),
        email=email or f'{uuid1()}@test.test',
        password=hash_password(password),
        is_admin=is_admin,
        is_teacher=is_teacher,
    )
    if commit:
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def create_course(
    db: Session,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    pass_percent: int | None = None,
    commit: bool = True,
):
    course = Course(
        name=name or str(uuid1()),
        description=description or str(uuid1()),
        pass_percent=pass_percent,
        competencies=[],
    )
    if commit:
        db.add(course)
        db.commit()
        db.refresh(course)
    return course


def create_user_course(
    db: Session,
    *,
    user_id: int,
    course_id: int,
    progress: int = 0,
    admission_date: datetime | None = None,
    commit: bool = True,
):
    user_course = UserCourse(
        user_id=user_id,
        course_id=course_id,
        progress=progress,
        admission_date=admission_date,
    )
    if commit:
        db.add(user_course)
        db.commit()
        db.refresh(user_course)
    return user_course


def get_records_count(
    *,
    route: str,
    client: Optional[Client] = None,
):
    client = client or login_as(test_admin)
    response = client.get(route)
    data = response.json()
    return len(data['items'])


def create_subdivision(
    db: Session,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    commit: bool = True,
):
    subdivision = Subdivision(
        name=name or str(uuid1()),
        description=description or str(uuid1()),
    )
    if commit:
        db.add(subdivision)
        db.commit()
        db.refresh(subdivision)
    return subdivision


def create_post(
    db: Session,
    *,
    subdivision_id: int | Column[int],
    name: Optional[str] = None,
    description: Optional[str] = None,
    commit: bool = True,
):
    subdivision = Post(
        name=name or str(uuid1()),
        description=description or str(uuid1()),
        subdivision_id=subdivision_id,
    )
    if commit:
        db.add(subdivision)
        db.commit()
        db.refresh(subdivision)
    return subdivision


def create_competence(
    db: Session,
    *,
    name: Optional[str] = None,
    courses: Optional[list[Course]] = None,
    posts: Optional[list[Post]] = None,
    commit: bool = True,
):
    courses = courses or []
    posts = posts or []

    competence = Competence(
        name=name or str(uuid1()),
        courses=courses,
        posts=posts,
    )
    if commit:
        db.add(competence)
        db.commit()
        db.refresh(competence)
    return competence


def create_topic(
    db: Session,
    *,
    course_id: int | Column[int],
    prev_topic_id: int | Column[int] | None = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    commit: bool = True,
):
    topic = Topic(
        name=name or str(uuid1()),
        description=description or str(uuid1()),
        course_id=course_id,
        prev_topic_id=prev_topic_id,
    )
    if commit:
        db.add(topic)
        db.commit()
        db.refresh(topic)
    return topic


def create_topic_resource(
    db: Session,
    *,
    topic_id: int | Column[int],
    prev_resource_id: int | Column[int] | None = None,
    type: TopicResourceType = TopicResourceType.text,
    name: Optional[str] = None,
    value: Optional[str] = None,
    commit: bool = True,
):
    resource = TopicResource(
        type=type,
        name=name or str(uuid1()),
        value=value or str(uuid1()),
        topic_id=topic_id,
        prev_resource_id=prev_resource_id,
    )
    if commit:
        db.add(resource)
        db.commit()
        db.refresh(resource)
    return resource


def create_task(
    db: Session,
    *,
    topic_id: int | Column[int],
    task_type: TaskType = TaskType.single,
    name: str | Column[str] | None = None,
    description: str | Column[str] | None = None,
    prev_task_id: int | Column[int] | None = None,
    commit: bool = True,
):
    task = Task(
        topic_id=topic_id,
        task_type=task_type,
        name=name or str(uuid1()),
        description=description or str(uuid1()),
        prev_task_id=prev_task_id,
    )
    if commit:
        db.add(task)
        db.commit()
        db.refresh(task)
    return task


def create_answer(
    db: Session,
    *,
    task_id: int | Column[int],
    value: str | Column[str] | None = None,
    is_correct: bool = False,
    commit: bool = True,
):
    answer = Answer(
        task_id=task_id,
        value=value or str(uuid1()),
        is_correct=is_correct,
    )
    if commit:
        db.add(answer)
        db.commit()
        db.refresh(answer)
    return answer
