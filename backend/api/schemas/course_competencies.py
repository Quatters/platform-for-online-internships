from backend.api.schemas.base import BaseSchema


class CourseCompetence(BaseSchema):
    id: int
    course_id: int
    course_name: str
    competence_id: int
    competence_name: str


class CreateCourseCompetence(BaseSchema):
    competence_id: int
