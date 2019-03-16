from marshmallow import Schema, fields, post_load
from marshmallow.fields import Nested, String, Integer, Boolean

from dtos.dtos import CodeExecutionRequestDto, FunctionDto
from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function_parameter import FunctionArgument
from models.language_enum import LanguageEnum
from models.test_question_template import TestQuestionTemplate
from models.test_template import TestTemplate


class ArgumentTypeSchema(Schema):
    name = String(required=True)

    @post_load()
    def create_class(self, value):
        name = value['name']
        return ArgumentType[name]


class FunctionArgumentDtoSchema(Schema):
    id = Integer(required=False, allow_none=True)
    type = Nested(ArgumentTypeSchema)
    name = String()

    @post_load()
    def create_class(self, value):
        return FunctionArgument(**value)


class LanguageSchema(Schema):
    name = String(required=True)

    @post_load()
    def create_class(self, value):
        name = value['name']
        return LanguageEnum[name]


class FunctionDtoSchema(Schema):
    id = Integer(required=False, allow_none=True)
    name = String(required=True)
    return_type = Nested(ArgumentTypeSchema,
                         load_from='returnType',
                         dump_to='returnType',
                         attribute='return_type')

    arguments = Nested(FunctionArgumentDtoSchema,
                       required=False,
                       load_from='arguments',
                       dump_to='arguments',
                       many=True,
                       )

    testing_input = Nested("FunctionTestingInputDtoSchema",
                           required=False,
                           allow_none=True,
                           load_from='testingInput',
                           dump_to='testingInput')  # type: "FunctionTestingInputDtoSchema"

    @post_load()
    def create_class(self, value):
        return FunctionDto(**value)


class CodeSnippetSchema(Schema):
    id = Integer(required=False, allow_none=True)
    language = Nested(LanguageSchema,
                      required=False,
                      allow_none=True)
    code = String(required=False,
                  allow_none=True
                  )
    function = Nested(FunctionDtoSchema,
                      required=False,
                      allow_none=True,
                      load_from="function",
                      dump_to="function")

    @post_load()
    def create_class(self, value):
        return CodeSnippet(**value)


class TestQuestionTemplateSchema(Schema):
    id = String(required=False, allow_none=True)
    name = String(required=False)
    description = String(required=False)
    time_limit = Integer(load_from='timeLimit',
                         dump_to='timeLimit',
                         attribute='time_limit',
                         required=False,
                         allow_none=True)
    version = Integer(required=False, allow_none=True)
    solution_code_snippet = Nested(CodeSnippetSchema,
                                   load_from='codeSnippet',
                                   dump_to='codeSnippet',
                                   attribute='solution_code_snippet')

    @post_load()
    def create_class(self, value):
        return TestQuestionTemplate(**value)


class TestTemplateDtoSchema(Schema):
    id = fields.Integer(required=False, allow_none=True)
    name = fields.String()
    time_limit = Integer(load_from='timeLimit',
                         dump_to='timeLimit',
                         attribute='time_limit',
                         allow_none=True)
    questions = Nested(TestQuestionTemplateSchema,
                       load_from='questionTemplates',
                       dump_to='questionTemplates',
                       attribute='questions',
                       many=True)
    is_deleted = Boolean(required=False,
                         allow_none=True,
                         load_from='isDeleted',
                         dump_to='isDeleted',
                         )

    @post_load()
    def create_class(self, value):
        template = TestTemplate(**value)
        return template


class FunctionScaffoldingDtoSchema(Schema):
    function = Nested(FunctionDtoSchema, required=True,
                      dump_to='function',
                      load_from='function')
    language = Nested(LanguageSchema, required=True)
    code = String(required=True)


class CodeExecutionRequestSchema(Schema):
    language = Nested(LanguageSchema,
                      required=True,
                      allow_none=False)

    return_type = Nested(ArgumentTypeSchema,
                         required=False,
                         allow_none=True,
                         load_from='returnType',
                         dump_to='returnType')

    function_id = Integer(required=False,
                          allow_none=True,
                          load_from='functionId',
                          dump_to='functionId')

    is_plain_code = Boolean(required=True,
                            allow_none=False,
                            load_from='isPlainCode',
                            dump_to='isPlainCode')

    code = String(required=True)

    client_id = String(required=False,
                       allow_none=True,
                       load_from='clientId',
                       dump_to='clientId')

    @post_load
    def create_class(self, value):
        return CodeExecutionRequestDto(**value)


class CodeRunResultSchema(Schema):
    language = Nested(LanguageSchema, required=True)
    output = String(required=True, allow_none=False)
    output_type = Nested(ArgumentTypeSchema, required=True,
                         allow_none=False,
                         load_from='outputType',
                         dump_to='outputType')
    error = String(required=True, allow_none=False)


class CodeExecutionResponseSchema(Schema):
    code_run_result = Nested(CodeRunResultSchema,
                             required=True,
                             allow_none=False,
                             dump_to='codeRunResult',
                             load_from='codeRunResult')

    client_id = String(required=False,
                       allow_none=True,
                       load_from='clientId',
                       dump_to='clientId')
