from typing import Optional
from uuid import uuid1
from httpx import Client
from sqlalchemy import Column
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import (
    Course,
    Competence,
    Topic,
    TopicResource,
    Subdivision,
)
from backend.constants import TopicResourceType
from tests.base import login_as, test_admin


def create_course(
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: Optional[Session] = None,
    commit: bool = True,
):
    db = db or next(get_db())
    course = Course(
        name=name or str(uuid1()),
        description=description or str(uuid1()),
        competencies=[],
    )
    if commit:
        db.add(course)
        db.commit()
        db.refresh(course)
    return course


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
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: Optional[Session] = None,
    commit: bool = True,
):
    db = db or next(get_db())
    subdivision = Subdivision(
        name=name or str(uuid1()),
        description=description or str(uuid1()),
    )
    if commit:
        db.add(subdivision)
        db.commit()
        db.refresh(subdivision)
    return subdivision


def create_competence(
    *,
    name: Optional[str] = None,
    courses: Optional[list[int]] = None,
    posts: Optional[list[int]] = None,
    db: Optional[Session] = None,
    commit: bool = True,
):
    db = db or next(get_db())
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
    *,
    course_id: int | Column[int],
    prev_topic_id: int | Column[int] | None = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    db: Optional[Session] = None,
    commit: bool = True,
):
    db = db or next(get_db())
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
    *,
    topic_id: int | Column[int],
    prev_resource_id: int | Column[int] | None = None,
    type: TopicResourceType = TopicResourceType.text,
    name: Optional[str] = None,
    value: Optional[str] = None,
    db: Optional[Session] = None,
    commit: bool = True,
):
    db = db or next(get_db())
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
