from typing import Tuple

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
    def try_from_string(type_, value, parse_str=True) -> Tuple[bool, any]:
        try:
            return True, ValueConverter.from_string(type_, value, parse_str)
        except:
            return False, None

    @staticmethod
    def from_string(type_, value, parse_str=True):
        if value is None:
            return None

        if type_ is ArgumentType.STRING:
            if not parse_str:
                return value
            if value == "":
                return value
            return json.loads(value)
        elif type_ is ArgumentType.INTEGER:
            return int(value)
        elif type_ is ArgumentType.ARRAY_STRING:
            return json.loads(value)
        elif type_ is ArgumentType.ARRAY_INTEGER:
            return json.loads(value)
        elif type_ is ArgumentType.VOID:
            return value
        else:
            raise NotImplemented

    @staticmethod
    def to_string(type_, value):
        return json.dumps(value)
