from . import (
    courses,
    users,
    user_courses,
    topics,
    tasks,
    answers,
    subdivisions,
    posts,
    competencies,
    topic_resources,
)

routers = (
    courses.router,
    users.router,
    user_courses.router,
    topics.router,
    tasks.router,
    answers.router,
    subdivisions.router,
    posts.router,
    competencies.router,
    topic_resources.router,
)
