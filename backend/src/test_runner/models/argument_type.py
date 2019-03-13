import enum


class ArgumentType(enum.Enum):
    Unset = 0
    VOID = 1
    INTEGER = 2
    STRING = 3
    ARRAY_INTEGER = 4
    ARRAY_STRING = 5
