from . import (
    courses,
    users,
    user_courses,
    topics,
    tasks,
)

routers = (
    courses.router,
    users.router,
    user_courses.router,
    topics.router,
    tasks.router,
)
