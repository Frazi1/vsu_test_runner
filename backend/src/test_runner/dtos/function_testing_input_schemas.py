from typing import List

from marshmallow import Schema, post_load
from marshmallow.fields import Integer, Nested, String

from dtos.schemas import ArgumentTypeSchema
from models.argument_type import ArgumentType
from models.function_inputs.base_function_input import DeclarativeFunctionInput
from models.function_inputs.declarative_input_argument_item import DeclarativeInputArgumentItem
from models.function_inputs.declarative_input_item import DeclarativeInputItem


class DeclarativeInputArgumentItemSchema(Schema):
    id = Integer(required=True,
                 allow_none=False,
                 dump_only=True)  # type: int

    argument_index = Integer(required=True,
                             allow_none=False,
                             dump_to='argumentIndex',
                             load_from='argumentIndex')  # type: int

    input_type = Nested(ArgumentTypeSchema,
                        required=True,
                        allow_none=False,
                        load_from='inputType',
                        dump_to='inputType')  # type: ArgumentType

    input_value = String(required=True,
                         allow_none=False,
                         dump_to='inputValue',
                         load_from='inputValue')  # type: str

    @post_load()
    def create_class(self, value):
        return DeclarativeInputArgumentItem(**value)


class DeclarativeInputItemSchema(Schema):
    id = Integer(required=True,
                 allow_none=False,
                 dump_only=True)  # type: int

    output_value = String(required=True,
                          allow_none=False,
                          load_from='outputValue',
                          dump_to='outputValue')  # type: str

    argument_items = Nested(DeclarativeInputArgumentItemSchema,
                            many=True,
                            allow_none=False,
                            required=True,
                            load_from='argumentItems',
                            dump_to='argumentItems')  # type: List[DeclarativeInputArgumentItem]

    @post_load()
    def create_class(self, value):
        return DeclarativeInputItem(**value)


class DeclarativeFunctionInputSchema(Schema):
    id = Integer(required=True,
                 allow_none=False,
                 dump_only=True)

    # target_function_id = Integer(required=True,
    #                              allow_none=False,
    #                              load_from='functionId',
    #                              dump_to='functionId')

    items = Nested(DeclarativeInputItemSchema, many=True, required=True)  # type: List[DeclarativeInputItem]

    @post_load()
    def create_class(self, value):
        return DeclarativeFunctionInput(**value)


class FunctionTestingInputDtoSchema(Schema):
    declarative_input = Nested(DeclarativeFunctionInputSchema,
                               load_from='declarativeInput',
                               dump_to='declarativeInput')  # type: DeclarativeFunctionInput
