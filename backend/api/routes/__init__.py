from . import (
    courses,
    users,
    user_courses,
)

routers = (
    courses.router,
    users.router,
    user_courses.router
)
