import enum
from functools import cached_property, cache
from backend.settings import TASKS_TIME


class BaseEnum(enum.Enum):
    def __str__(self):
        return self.value


class TaskType(BaseEnum):
    single = 'single'
    multiple = 'multiple'
    text = 'text'
    excel = 'excel'

    @cache
    def may_have_answers(self):
        return self in [TaskType.single, TaskType.multiple]

    @cached_property
    def time_to_pass(self):
        return TASKS_TIME[self.value]


class TopicResourceType(BaseEnum):
    text = 'text'
    image = 'image'
    video = 'video'
    embedded = 'embedded'
