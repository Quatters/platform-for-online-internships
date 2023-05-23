from sqlalchemy import Column, String
from backend.models import BaseModel


class Competence(BaseModel):
    name = Column(String, nullable=False, unique=True, index=True)
