from pydantic import BaseModel as PydanticBaseSchema


class BaseSchema(PydanticBaseSchema):
    class Config:
        orm_mode = True
