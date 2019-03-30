import enum


class ExecutionType(enum.Enum):
    PLAIN_TEXT = 1
    DEFAULT_TEMPLATE = 2
    CUSTOM_TEMPLATE = 3
    ONE_BY_ONE = 4