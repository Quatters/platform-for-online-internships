from . import (
    courses,
    users,
    user_courses,
    subdivisions,
    posts,
)

routers = (
    courses.router,
    users.router,
    user_courses.router,
    subdivisions.router,
    posts.router,
)
