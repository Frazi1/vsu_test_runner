from typing import List

from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function import Function
from models.function_inputs.base_function_input import DeclarativeFunctionInput, BaseFunctionInput
from models.function_inputs.declarative_input_argument_item import DeclarativeInputArgumentItem
from models.function_inputs.declarative_input_item import DeclarativeInputItem
from models.function_parameter import FunctionArgument
from models.language_enum import LanguageEnum
from models.question_answer import QuestionAnswer
from models.test_question_template import TestQuestionTemplate
from models.test_run import TestRun
from models.test_template import TestTemplate
from utils.pyjson.pyjson import BaseJsonable, JsonProperty


class LanguageDto(BaseJsonable):
    __exportables__ = {
        "name": JsonProperty(LanguageEnum)
    }

    def __init__(self, name=None):
        self.name = name


class ArgumentTypeDto(BaseJsonable):
    __exportables__ = {
        "name": JsonProperty(ArgumentType)
    }

    def __init__(self, name=None):
        self.name = name


class TestTemplateDto(object):
    def __init__(self, id_, name, time_limit, question_dtos, is_deleted, *args, **kwargs):
        super(TestTemplateDto, self).__init__(*args, **kwargs)

        self.id = id_  # type: int
        self.questions = question_dtos  # type: List[TestQuestionTemplateDto]
        self.is_deleted = is_deleted  # type: bool
        self.time_limit = time_limit  # type: int
        self.name = name  # type:str

    @staticmethod
    def list_of(test_templates):
        res = [TestTemplateDto.from_entity(x) for x in test_templates]
        return res

    @classmethod
    def from_entity(cls, e):
        # type: (TestTemplate) -> TestTemplateDto
        res = cls(e.id, e.name, e.time_limit, TestQuestionTemplateDto.from_list(e.questions), e.is_deleted)
        return res

    def to_entity(self):
        return TestTemplate(self.id, self.name, self.time_limit, [x.to_entity() for x in self.questions])


class TestQuestionTemplateDto(object):

    def __init__(self, id_, name, description, time_limit, solution_code_snippet_dto, version, is_deleted):
        self.is_deleted = is_deleted  # type: bool
        self.version = version  # type: int
        self.time_limit = time_limit  # type: int
        self.description = description  # type: str
        self.name = name  # type: str
        self.id_ = id_  # type: int
        self.solution_code_snippet = solution_code_snippet_dto  # type: CodeSnippetDto

    @classmethod
    def from_entity(cls, e):
        # type: (TestQuestionTemplate) -> TestQuestionTemplateDto
        res = cls(e.id, e.name,
                  e.description,
                  e.time_limit,
                  CodeSnippetDto.from_entity(e.solution_code_snippet),
                  e.version, e.is_deleted)
        return res

    @classmethod
    def from_list(cls, list_e):
        # type: (List[TestQuestionTemplate]) -> List[TestQuestionTemplateDto]
        res = [TestQuestionTemplateDto.from_entity(x) for x in list_e]
        return res

    def to_entity(self):
        return TestQuestionTemplate(self.id_, self.name, self.description, self.time_limit,
                                    self.solution_code_snippet.to_entity(), self.version, self.is_deleted)


class CodeRunResult(object):
    __exportables__ = {
        "language": JsonProperty(LanguageEnum),
        "output": JsonProperty(str),
        "output_type": JsonProperty(ArgumentType, "outputType"),
        "error": JsonProperty(str)
    }
    def __init__(self, language, output, output_type, error=None):
        self.language = language
        self.output = output
        self.output_type = output_type
        self.error = error


class TestRunQuestionAnswerDto(object):
    def __init__(self, id, name, description, answer_code_snippet, function_id):
        self.id = id
        self.name = name
        self.description = description
        self.answer_code_snippet = answer_code_snippet
        self.function_id = function_id

    @classmethod
    def map_from(cls, question_answer):
        # type: (QuestionAnswer) -> TestRunQuestionAnswerDto
        cls_ = cls(id=question_answer.id,
                   name=question_answer.question_instance.name,
                   description=question_answer.question_instance.description,
                   answer_code_snippet=question_answer.code_snippet,
                   function_id=question_answer.question_instance.solution_code_snippet.function_id)
        return cls_


class TestRunDto(object):
    def __init__(self, id, name, started_at, ends_at, finished_at, time_limit, question_answers):
        self.id = id
        self.name = name
        self.started_at = started_at
        self.ends_at = ends_at
        self.finished_at = finished_at
        self.time_limit = time_limit
        self.question_answers = question_answers

    @classmethod
    def map_from(cls, test_run):
        # type: (TestRun) -> TestRunDto
        cls_ = cls(id=test_run.id,
                   name=test_run.test_instance.name,
                   started_at=test_run.started_at,
                   ends_at=test_run.ends_at,
                   finished_at=test_run.finished_at,
                   time_limit=test_run.test_instance.time_limit,
                   question_answers=[TestRunQuestionAnswerDto.map_from(x) for x in test_run.question_answers])
        return cls_


class TestInstanceUpdate(object):
    def __init__(self, available_after, disabled_after, time_limit):
        self.available_after = available_after
        self.disabled_after = disabled_after
        self.time_limit = time_limit


class FunctionScaffoldingDto(object):
    def __init__(self, code, language, function):
        self.function = function
        self.language = language
        self.code = code


class CodeExecutionRequestDto(BaseJsonable):
    __exportables__ ={
        "return_type": JsonProperty(ArgumentType, "returnType"),
        "function_id": JsonProperty(int, "functionId", required=False),
        "language": JsonProperty(LanguageEnum),
        "code": JsonProperty(str),
        "is_plain_code": JsonProperty(bool, "isPlainCode"),
        "client_id": JsonProperty(str, "clientId", required=False)
    }

    def __init__(self, code='', language=None, is_plain_code=None, client_id=None, function_id=None, return_type=None):
        # type: (str, LanguageEnum, bool, str | None, int, ArgumentType) -> None

        self.return_type = return_type  # type: ArgumentType
        self.function_id = function_id  # type: int
        self.language = language  # type: LanguageEnum
        self.code = code  # type: str
        self.is_plain_code = is_plain_code  # type: bool
        self.client_id = client_id  # type: str|None


class CodeExecutionResponseDto(object):
    __exportables__ = {
        "code_run_result": JsonProperty(CodeRunResult, "codeRunResult"),
        "client_id": JsonProperty(str, "clientId")
    }
    def __init__(self, code_run_result, client_id=None):
        # type: (CodeRunResult, str) -> None

        self.code_run_result = code_run_result
        self.client_id = client_id


class CreateFunctionTestingInputRequestDto(object):
    def __init__(self, function_id, declarative_input):
        # type: (int, DeclarativeFunctionInput) -> None
        self.function_id = function_id
        self.declarative_input = declarative_input


class CodeSnippetDto(object):
    def __init__(self, id_, language, code, function_dto, *args, **kwargs):
        super(CodeSnippetDto, self).__init__(*args, **kwargs)
        self.id = id_  # type: int
        self.function = function_dto  # type: FunctionDto
        self.code = code  # type: str
        self.language = language  # type: LanguageEnum

    @classmethod
    def from_entity(cls, s):
        # type: (CodeSnippet) -> CodeSnippetDto
        res = cls(s.id, s.language, s.code, FunctionDto.from_function(s.function))
        return res

    def to_entity(self):
        res = CodeSnippet(self.id, self.language, self.code, self.function.to_entity())
        return res


class FunctionDto(object):
    def __init__(self, id=None, name=None, return_type=None, argument_dtos=None, function_input_dto=None, *args,
                 **kwargs):
        super(FunctionDto, self).__init__(*args, **kwargs)
        self.testing_input = function_input_dto  # type: FunctionInputDto
        self.arguments = argument_dtos  # type: List[FunctionArgumentDto]
        self.return_type = return_type  # type: ArgumentType
        self.name = name  # type: str
        self.id = id  # type: int

    @classmethod
    def from_function(cls, function):
        # type: (Function) -> FunctionDto
        res = cls(function.id,
                  function.name,
                  function.return_type,
                  FunctionArgumentDto.list_of(function.arguments),
                  FunctionInputDto.from_entity(function.testing_input))
        return res

    def to_entity(self):
        res = Function(self.id, self.name, self.return_type, [x.to_entity() for x in self.arguments],
                       self.testing_input.to_entity())
        return res


class FunctionArgumentDto(object):
    def __init__(self, id_, type_, name, *args, **kwargs):
        super(FunctionArgumentDto, self).__init__(*args, **kwargs)
        self.name = name
        self.type = type_
        self.id = id_

    @classmethod
    def from_entity(cls, e):
        # type: (FunctionArgument) -> FunctionArgumentDto
        res = cls(e.id, e.type, e.name)
        return res

    @classmethod
    def list_of(cls, e_list):
        return [FunctionArgumentDto.from_entity(x) for x in e_list]

    def to_entity(self):
        pass


class FunctionInputDto(object):
    def __init__(self, id_, declarative_input=None):
        self.declarative_input = declarative_input  # type: DeclarativeFunctionInputDto
        self.id_ = id_

    @classmethod
    def from_entity(cls, e):
        # type: (BaseFunctionInput) -> FunctionInputDto | None
        if not e:
            return None

        res = cls(e.id)
        if isinstance(e, DeclarativeFunctionInput):
            res.declarative_input = DeclarativeFunctionInputDto.from_entity(e)
        return res

    def to_entity(self):
        if self.declarative_input:
            return DeclarativeFunctionInput(items=[x.to_entity() for x in self.declarative_input.items])


class DeclarativeFunctionInputDto(object):
    def __init__(self, declarative_items_dtos):
        self.items = declarative_items_dtos  # type: List[DeclarativeInputItemDto]

    @classmethod
    def from_entity(cls, e):
        # type: (DeclarativeFunctionInput) -> DeclarativeFunctionInputDto
        res = cls(DeclarativeInputItemDto)
        return res


class DeclarativeInputItemDto(object):
    def __init__(self, id_, declarative_argument_item_dtos, output_value):
        self.id_ = id_  # type: int
        self.declarative_argument_item_dtos = declarative_argument_item_dtos  # type: List[DeclarativeInputArgumentItemDto]
        self.output_value = output_value  # type: str

    @classmethod
    def from_entity(cls, e):
        # type: (DeclarativeInputItem) -> DeclarativeInputItemDto
        res = cls(e.id, DeclarativeInputArgumentItemDto.from_list(e.argument_items), e.output_value)
        return res

    @classmethod
    def from_list(cls, list_e):
        # type: (List[DeclarativeInputItem]) -> List[DeclarativeInputItemDto]
        res = [DeclarativeInputItemDto.from_entity(x) for x in list_e]
        return res

    def to_entity(self):
        # type: () -> DeclarativeInputItem
        res = DeclarativeInputItem(self.id_, [x.to_entity() for x in self.declarative_argument_item_dtos],
                                   self.output_value)
        return res


class DeclarativeInputArgumentItemDto(object):
    def __init__(self, id_, argument_index, input_type, input_value):
        self.id_ = id_  # type: int
        self.argument_index = argument_index  # type: int
        self.input_type = input_type  # type: ArgumentType
        self.input_value = input_value  # type: str

    @classmethod
    def from_entity(cls, e):
        # type: (DeclarativeInputArgumentItem) -> DeclarativeInputArgumentItemDto
        res = cls(e.id, e.argument_index, e.input_type, e.input_value)
        return res

    @classmethod
    def from_list(cls, list_e):
        # type: (List[DeclarativeInputArgumentItem]) -> List[DeclarativeInputArgumentItemDto]
        res = [DeclarativeInputArgumentItemDto.from_entity(x) for x in list_e]
        return res

    def to_entity(self):
        # type: ()-> DeclarativeInputArgumentItem
        res = DeclarativeInputArgumentItem(self.id_, self.argument_index, self.input_type, self.input_value)
        return res
