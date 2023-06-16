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


class TestAttemptStatus(BaseEnum):
    in_progress = 'in_progress'
    system_checking = 'system_checking'
    timeout_failure = 'timeout_failure'
    check_failure = 'check_failure'
    partially_checked = 'partially_checked'
    checked = 'checked'


class UserAnswerStatus(BaseEnum):
    checked = 'checked'
    unchecked = 'unchecked'
