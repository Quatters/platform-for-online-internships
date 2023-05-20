from sqlalchemy import Column, BigInteger
from backend.database import Base


def tablename(name: str):
    return f'app_{name.lower()}'


class BaseModelMeta(type(Base)):
    def __new__(cls, name, bases, attrs):
        if '__tablename__' not in attrs:
            # add prefix to avoid collisions with built-in names
            attrs['__tablename__'] = tablename(name)
        return super().__new__(cls, name, bases, attrs)


class BaseModel(Base, metaclass=BaseModelMeta):
    """
    Abstract base model which already has an `id` field. Also, if
    `__tablename__` is not set, it will be generated automatically as
    lower name of the class (e.g. class `BaseModel` -> table `basemodel`).
    """

    __abstract__ = True

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
