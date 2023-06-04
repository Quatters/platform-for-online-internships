import enum


class BaseEnum(enum.Enum):
    def __str__(self):
        return self.value


class TaskType(BaseEnum):
    single = 'single'
    multiple = 'multiple'
    text = 'text'
    excel = 'excel'

    def may_have_answers(self):
        return self in [TaskType.single, TaskType.multiple]


class TopicResourceType(BaseEnum):
    text = 'text'
    image = 'image'
    video = 'video'
    embedded = 'embedded'
