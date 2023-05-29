from backend.api.schemas.base import BaseSchema


class PostCompetence(BaseSchema):
    id: int
    post_id: int
    post_name: str
    competence_id: int
    competence_name: str


class CreatePostCompetence(BaseSchema):
    competence_id: int
