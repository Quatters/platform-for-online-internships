from . import (
    courses,
    users,
    user_courses,
    subdivisions,
)

routers = (
    courses.router,
    users.router,
    user_courses.router,
    subdivisions.router,
)
