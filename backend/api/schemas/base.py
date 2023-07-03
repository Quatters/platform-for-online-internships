from pydantic import BaseModel as PydanticBaseSchema


class BaseSchema(PydanticBaseSchema):
    class Config:
        orm_mode = True


class OkData(BaseSchema):
    detail: str = 'OK'
