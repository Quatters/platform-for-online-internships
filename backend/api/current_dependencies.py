from fastapi import Depends
from sqlalchemy.orm import Session
from backend.api.errors.errors import not_found
from backend.models.courses import Course
from backend.models.posts import Post
from backend.models.topics import Topic
from backend.database import get_db
import backend.api.queries.courses as queries_courses
import backend.api.queries.topics as queries_topics
import backend.api.queries.tasks as queries_tasks
import backend.api.queries.subdivisions as queries_subdivisions
import backend.api.queries.posts as queries_posts
import backend.api.queries.competencies as queries_competencies


def get_current_course(course_id: int, db: Session = Depends(get_db)):
    course = queries_courses.get_course(db, course_id)
    if course is None:
        raise not_found()
    return course


def current_topic(
        topic_id: int,
        course: Course = Depends(get_current_course),
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


def current_subdivision(subdivision_id: int, db: Session = Depends(get_db)):
    subdivision = queries_subdivisions.get_subdivision(db, subdivision_id)
    if subdivision is None:
        raise not_found()
    return subdivision


def current_post(post_id, db: Session = Depends(get_db)):
    post = queries_posts.get_post(db, post_id)
    if post is None:
        raise not_found()
    return post


async def get_current_competence(competence_id: int,
                                 db: Session = Depends(get_db)):
    competence = queries_competencies.get_competence(db, competence_id)
    if competence is None:
        raise not_found()
    return competence
