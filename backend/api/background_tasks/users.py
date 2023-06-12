from sqlalchemy.orm import Session, joinedload
from backend.models import User


def handle_user_teachers_after_post_change(db: Session):
    interns = db.query(User).filter(
        (User.teacher_id != None) & ~(User.is_teacher | User.is_admin)
    ).options(
        joinedload(User.posts),
        joinedload(User.teacher).options(
            joinedload(User.posts),
        )
    )

    for intern in interns:
        if not set(intern.posts).intersection(intern.teacher.posts):
            intern.teacher_id = None

    db.commit()
