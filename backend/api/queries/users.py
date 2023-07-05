from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import paginate as pypaginate
from backend.api.errors.errors import bad_request
from backend.models import Post, User, Course, UserCourse
from backend.models.association_tables import UserPostAssociation
from backend.api.dependencies import ListPageParams, UserListPageParams
from backend.api.queries.helpers import get_instances_or_400, with_search
from backend.api.queries.posts import get_mastered_posts
from backend.api.schemas import users as schemas
from backend.api.utils import hash_password


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).get(user_id)


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter_by(email=email).first()


def get_users(db: Session, params: UserListPageParams):
    query = db.query(User)

    if params.role == 'admin':
        query = query.filter(User.is_admin)
    elif params.role == 'teacher':
        query = query.filter(User.is_teacher)
    elif params.role == 'intern':
        query = query.filter(~(User.is_admin | User.is_teacher))

    query = with_search(
        User.email,
        User.first_name,
        User.last_name,
        User.patronymic,
        query=query,
        search=params.search,
    )
    return paginate(query, params)


def update_user(db: Session, user: User, patch_data: schemas.PatchUser):
    dict_ = patch_data.dict(exclude_unset=True)
    if 'posts' in dict_ and not user.is_admin:
        user.posts = get_instances_or_400(db, Post, dict_.pop('posts'))
    for key, value in dict_.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def create_user(db: Session, user: schemas.CreateUser):
    created_user = User(
        **user.dict(exclude={'posts', 'password'}),
        password=hash_password(user.password),
    )
    if not user.is_admin:
        created_user.posts = get_instances_or_400(db, Post, user.posts)
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user


def get_assigned_interns(db: Session, teacher_id: int, params: ListPageParams):
    query = db.query(User).filter(User.teacher_id == teacher_id)
    return with_search(
        User.email,
        User.first_name,
        User.last_name,
        User.patronymic,
        query=query,
        search=params.search,
    )


def get_paginated_assigned_interns(db: Session, teacher_id: int, params: ListPageParams):
    return paginate(
        get_assigned_interns(db, teacher_id, params),
        params,
    )


def _annotate_intern_with_stats(db: Session, intern: User):
    user_courses = db.query(UserCourse).filter(
        UserCourse.user_id == intern.id,
    ).options(
        joinedload(UserCourse.course),
    )
    intern.finished_courses = db.query(Course).filter(
        Course.id.in_(
            user_courses.filter(
                UserCourse.course.has(UserCourse.progress >= Course.pass_percent),
            ).with_entities(UserCourse.course_id),
        ),
    ).order_by(
        Course.name,
    ).all()
    intern.learnt_posts = get_mastered_posts(db, intern)
    total_score = user_courses.with_entities(func.sum(UserCourse.progress)).scalar() or 0
    count = user_courses.count() or 1
    intern.average_score = total_score / count
    return intern


def get_interns_with_stats(db: Session, teacher: User, params: ListPageParams):
    query = get_assigned_interns(db, teacher.id, params).options(
        joinedload(User.user_competencies),
        joinedload(User.posts),
    )
    interns = [_annotate_intern_with_stats(db, intern) for intern in query.all()]
    interns.sort(key=lambda intern: intern.average_score, reverse=True)
    return pypaginate(interns, length_function=lambda *_: query.count())


def get_assigned_intern(db: Session, teacher_id: int, intern_id: int):
    return db.query(User).filter(
        (User.teacher_id == teacher_id) & (User.id == intern_id)
    ).one_or_none()


def get_intern_with_stats(db: Session, intern_id: int, teacher: User):
    intern = get_assigned_intern(db, teacher.id, intern_id)
    if not intern:
        return intern
    return _annotate_intern_with_stats(db, intern)


def assign_interns(db: Session, teacher: User, intern_ids: list[int]):
    if db.query(db.query(User.id).filter(
        (User.teacher_id != None) & (User.id.in_(intern_ids))).exists()  # noqa: E711
    ).scalar():
        raise bad_request('One or more of the interns are already assigned to teacher.')

    interns = db.query(User).filter(User.id.in_(intern_ids)).options(
        joinedload(User.posts),
    ).all()
    teacher_posts = set(teacher.posts)

    for intern in interns:
        if not set(intern.posts).intersection(teacher_posts):
            raise bad_request(
                f'Intern {intern.email} (id: {intern.id}) cannot be assigned to this teacher because they '
                'have no matching posts.',
            )
        intern.teacher_id = teacher.id

    db.commit()

    return intern_ids


def unassign_intern(db: Session, intern_id: int):
    intern = get_user(db, intern_id)
    intern.teacher_id = None
    db.commit()


def get_suitable_for_assign_interns(db: Session, teacher: User, params: ListPageParams):
    teacher_post_ids_query = db.query(UserPostAssociation.c.post_id).filter(
        UserPostAssociation.c.user_id == teacher.id
    )
    suitable_user_ids_query = db.query(UserPostAssociation.c.user_id).filter(
        UserPostAssociation.c.post_id.in_(teacher_post_ids_query)
    )
    suitable_interns_query = db.query(User.id, User.email).filter(
        ~(User.is_admin | User.is_teacher)
        & (User.teacher_id == None)  # noqa: E711
        & (User.id.in_(suitable_user_ids_query))
    )
    query = with_search(User.email, query=suitable_interns_query, search=params.search)
    return paginate(query, params)
