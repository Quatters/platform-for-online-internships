from backend.api.schemas.base import BaseSchema
from backend.api.schemas.posts import Post


class FkCompetence(BaseSchema):
    id: int
    name: str


class FkUser(BaseSchema):
    id: int
    email: str


class FkCourse(BaseSchema):
    id: int
    name: str


class User(BaseSchema):
    id: int
    email: str
    first_name: str
    last_name: str
    patronymic: str
    is_admin: bool
    is_teacher: bool
    posts: list[Post]
    teacher: FkUser | None
    competencies: list[FkCompetence]


class ListUser(BaseSchema):
    id: int
    email: str
    first_name: str
    last_name: str
    patronymic: str
    is_admin: bool
    is_teacher: bool


class InternWithStats(ListUser):
    finished_courses: list[FkCourse]
    competencies: list[FkCompetence]
    posts: list[Post]
    learnt_posts: list[Post]
    average_score: float


class DbUser(User):
    password: str


class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    email: str | None = None


class PatchUser(BaseSchema):
    email: str | None
    first_name: str | None
    last_name: str | None
    patronymic: str | None
    posts: list[int] | None


class CreateUser(BaseSchema):
    email: str
    password: str
    first_name: str = ''
    last_name: str = ''
    patronymic: str = ''
    posts: list[int] = []
    is_admin: bool
    is_teacher: bool


class RegisterUser(CreateUser):
    is_admin: bool = False
    is_teacher: bool = False


class AssignInterns(BaseSchema):
    interns: list[int]
