from . import (
    courses,
    users,
    user_courses,
    topics,
    tasks,
    answers,
)

routers = (
    courses.router,
    users.router,
    user_courses.router,
    topics.router,
    tasks.router,
    answers.router,
)
