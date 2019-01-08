import ujson

from src.models.ArgumentType import ArgumentType


class ValueConverter:
    def __init__(self):
        pass

    @staticmethod
    def from_string(type_, value):
        if type_ is ArgumentType.STRING:
            return value
        elif type_ is ArgumentType.INTEGER:
            return int(value)
        elif type_ is ArgumentType.ARRAY_STRING:
            return ujson.loads(value)
        elif type_ is ArgumentType.ARRAY_INTEGER:
            return [int(x) for x in ujson.loads(value)]
        else:
            raise NotImplemented

    @staticmethod
    def to_string(type_, value):
        return ujson.dumps(value)
