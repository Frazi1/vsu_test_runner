import ujson

from models.argument_type import ArgumentType


class ValueConverter:
    def __init__(self):
        pass

    @staticmethod
    def from_string(type_, value):
        if type_ is ArgumentType.STRING:
            if value == "":
                return value
            return ujson.loads(value)
        elif type_ is ArgumentType.INTEGER:
            return int(value)
        elif type_ is ArgumentType.ARRAY_STRING:
            return ujson.loads(value)
        elif type_ is ArgumentType.ARRAY_INTEGER:
            return ujson.loads(value)
        else:
            raise NotImplemented

    @staticmethod
    def to_string(type_, value):
        return ujson.dumps(value)
