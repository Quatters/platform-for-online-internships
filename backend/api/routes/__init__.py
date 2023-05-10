from . import (
    courses,
    users,
    user_courses,
    topics,
)

routers = (
    courses.router,
    users.router,
    user_courses.router,
    topics.router,
)
