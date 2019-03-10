from models.argument_type import ArgumentType


class FunctionRunArgument(object):
    def __init__(self, argument_type, argument_value):
        self.argument_value = argument_value  # type: str
        self.argument_type = argument_type  # type: ArgumentType
