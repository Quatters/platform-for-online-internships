from fastapi import Depends
from sqlalchemy.orm import Session
from backend.api.errors.errors import not_found
from backend.api.schemas.courses import Course
from backend.api.schemas.topics import Topic
from backend.database import get_db
import backend.api.queries.courses as queries_courses
import backend.api.queries.topics as queries_topics
import backend.api.queries.tasks as queries_tasks
import backend.api.queries.topic_resources as queries_topic_resources


def current_course(course_id: int, db: Session = Depends(get_db)):
    course = queries_courses.get_course(db, course_id)
    if course is None:
        raise not_found()
    return course


def current_topic(
        topic_id: int,
        course: Course = Depends(current_course),
        db: Session = Depends(get_db)):
    topic = queries_topics.get_topic(db, topic_id)
    if topic is None or topic.course_id != course.id:
        raise not_found()
    return topic


def current_task(
        task_id: int,
        topic: Topic = Depends(current_topic),
        db: Session = Depends(get_db)):
    task = queries_tasks.get_task(db, task_id)
    if task is None or task.topic_id != topic.id:
        raise not_found()
    return task


def current_topic_resource(
    resource_id: int,
    topic: Topic = Depends(current_topic),
    db: Session = Depends(get_db),
):
    resource = queries_topic_resources.get_topic_resource(db, resource_id)
    if resource is None or resource.topic_id != topic.id:
        raise not_found()
    return resource
