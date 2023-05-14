import enum

class TaskType(enum.Enum):
    single = 'single'
    multiple = 'multiple'
    text = 'text'
    excel = 'excel'


    def __str__(self):
        return self.value
