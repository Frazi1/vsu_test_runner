try:
    import ujson
    json = ujson
except:
    import json
    json = json

from models.argument_type import ArgumentType


class ValueConverter:
    def __init__(self):
        pass

    @staticmethod
    def from_string(type_, value):
        if type_ is ArgumentType.STRING:
            if value == "":
                return value
            return json.loads(value)
        elif type_ is ArgumentType.INTEGER:
            return int(value)
        elif type_ is ArgumentType.ARRAY_STRING:
            return json.loads(value)
        elif type_ is ArgumentType.ARRAY_INTEGER:
            return json.loads(value)
        else:
            raise NotImplemented

    @staticmethod
    def to_string(type_, value):
        return json.dumps(value)
