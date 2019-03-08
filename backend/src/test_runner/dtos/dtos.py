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


class BaseDto(BaseJsonable):
    def __init__(self, **kwargs):
        for name, value in kwargs.iteritems():
            setattr(self, name, value)


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


class TestQuestionTemplateDto(BaseDto):
    __exportables__ = {
        "is_deleted": JsonProperty(bool, dump_name='isDeleted'),
        "version": JsonProperty(int),
        "time_limit": JsonProperty(int, dump_name='timeLimit', required=False),
        "description": JsonProperty(str),
        "id": JsonProperty(int, required=False),
        "solution_code_snippet": JsonProperty("CodeSnippetDto", dump_name='solutionCodeSnippet')
    }

    is_deleted = None  # type: bool
    version = None  # type: int
    time_limit = None  # type: int
    description = None  # type: str
    name = None  # type: str
    id = None  # type: int
    solution_code_snippet = None  # type: CodeSnippetDto

    @classmethod
    def from_entity(cls, e):
        # type: (TestQuestionTemplate) -> TestQuestionTemplateDto
        res = cls(id=e.id, name=e.name,
                  description=e.description,
                  time_limit=e.time_limit,
                  solution_code_snippet=CodeSnippetDto.from_entity(e.solution_code_snippet),
                  version=e.version, is_deleted=e.is_deleted)
        return res

    @classmethod
    def from_list(cls, list_e):
        # type: (List[TestQuestionTemplate]) -> List[TestQuestionTemplateDto]
        res = [TestQuestionTemplateDto.from_entity(x) for x in list_e]
        return res

    def to_entity(self):
        return TestQuestionTemplate(self.id, self.name, self.description, self.time_limit,
                                    self.solution_code_snippet.to_entity(), self.version, self.is_deleted)


class TestTemplateDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "questions": JsonProperty([TestQuestionTemplateDto]),
        "is_deleted": JsonProperty(bool, dump_name="isDeleted", required=False),
        "time_limit": JsonProperty(int, required=False),
        "name": JsonProperty(str)
    }

    id = None  # type: int
    questions = None  # type: List[TestQuestionTemplateDto]
    is_deleted = None  # type: bool
    time_limit = None  # type: int
    name = None  # type:str

    @staticmethod
    def list_of(test_templates):
        res = [TestTemplateDto.from_entity(x) for x in test_templates]
        return res

    @classmethod
    def from_entity(cls, e):
        # type: (TestTemplate) -> TestTemplateDto
        res = cls(id=e.id, name=e.name, time_limit=e.time_limit,
                  questions=TestQuestionTemplateDto.from_list(e.questions), is_deleted=e.is_deleted)
        return res

    def to_entity(self):
        return TestTemplate(self.id, self.name, self.time_limit, [x.to_entity() for x in self.questions])


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
    __exportables__ = {
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
        self.client_id = client_id  # type: (str|None)


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


class CodeSnippetDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "function": JsonProperty("FunctionDto"),
        "code": JsonProperty(str),
        "language": JsonProperty(LanguageEnum)
    }

    id = None  # type: int
    function = None  # type: FunctionDto
    code = None  # type: str
    language = None  # type: LanguageEnum

    @classmethod
    def from_entity(cls, s):
        # type: (CodeSnippet) -> CodeSnippetDto
        res = cls(id=s.id, language=s.language, code=s.code, function=FunctionDto.from_function(s.function))
        return res

    def to_entity(self):
        res = CodeSnippet(id=self.id, language=self.language, code=self.code, function=self.function.to_entity())
        return res


class FunctionDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "return_type": JsonProperty(ArgumentType),
        "name": JsonProperty(str),
        "arguments": JsonProperty(["FunctionArgumentDto"]),
        "testing_input": JsonProperty("FunctionInputDto", dump_name="testingInput")
    }
    testing_input = None
    arguments = None
    return_type = None
    name = None
    id = None

    @classmethod
    def create(cls, id_=None, name=None, return_type=None, argument_dtos=None, function_input_dto=None):
        res = cls()
        res.id = id_
        res.testing_input = function_input_dto  # type: FunctionInputDto
        res.arguments = argument_dtos  # type: List[FunctionArgumentDto]
        res.return_type = return_type  # type: ArgumentType
        res.name = name  # type: str  # type: int
        return res

    @classmethod
    def from_function(cls, function):
        # type: (Function) -> FunctionDto
        res = cls.create(function.id,
                         function.name,
                         function.return_type,
                         FunctionArgumentDto.list_of(function.arguments),
                         FunctionInputDto.from_entity(function.testing_input))
        return res

    def to_entity(self):
        res = Function(self.id, self.name, self.return_type, [x.to_entity() for x in self.arguments],
                       self.testing_input.to_entity())
        return res


class FunctionArgumentDto(BaseDto):
    __exportables__ = {
        "name": JsonProperty(str),
        "type": JsonProperty(ArgumentType),
        "id": JsonProperty(int, required=False)
    }
    name = None  # type: str
    type = None  # type: ArgumentType
    id = None  # type: int

    @classmethod
    def from_entity(cls, e):
        # type: (FunctionArgument) -> FunctionArgumentDto
        res = cls(id=e.id, type=e.type, name=e.name)
        return res

    @classmethod
    def list_of(cls, e_list):
        return [FunctionArgumentDto.from_entity(x) for x in e_list]

    def to_entity(self):
        pass


class FunctionInputDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "declarative_input": JsonProperty("DeclarativeFunctionInputDto", dump_name="declarativeInput")
    }
    declarative_input = None  # type: DeclarativeFunctionInputDto
    id = None  # type: int

    @classmethod
    def from_entity(cls, e):
        # type: (BaseFunctionInput) -> FunctionInputDto | None
        if not e:
            return None

        res = cls(id=e.id)
        if isinstance(e, DeclarativeFunctionInput):
            res.declarative_input = DeclarativeFunctionInputDto.from_entity(e)
        return res

    def to_entity(self):
        if self.declarative_input:
            return DeclarativeFunctionInput(items=[x.to_entity() for x in self.declarative_input.items])


class DeclarativeFunctionInputDto(BaseDto):
    __exportables__ = {
        "items": JsonProperty(["DeclarativeInputItemDto"])
    }
    items = None  # type: List[DeclarativeInputItemDto]

    @classmethod
    def from_entity(cls, e):
        # type: (DeclarativeFunctionInput) -> DeclarativeFunctionInputDto
        res = cls(items=DeclarativeInputItemDto)
        return res


class DeclarativeInputItemDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int),
        "declarative_argument_item_dtos": JsonProperty(["DeclarativeInputArgumentItemDto"], dump_name="argumentItems")
    }
    id = None  # type: int
    declarative_argument_item_dtos = None  # type: List[DeclarativeInputArgumentItemDto]
    output_value = None  # type: str

    @classmethod
    def from_entity(cls, e):
        # type: (DeclarativeInputItem) -> DeclarativeInputItemDto
        res = cls(id=e.id, declarative_argument_item_dtos=DeclarativeInputArgumentItemDto.from_list(e.argument_items),
                  output_value=e.output_value)
        return res

    @classmethod
    def from_list(cls, list_e):
        # type: (List[DeclarativeInputItem]) -> List[DeclarativeInputItemDto]
        res = [DeclarativeInputItemDto.from_entity(x) for x in list_e]
        return res

    def to_entity(self):
        # type: () -> DeclarativeInputItem
        res = DeclarativeInputItem(self.id, [x.to_entity() for x in self.declarative_argument_item_dtos],
                                   self.output_value)
        return res


class DeclarativeInputArgumentItemDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "argument_index": JsonProperty(int, dump_name="argumentIndex"),
        "input_type": JsonProperty(ArgumentType, dump_name="argumentIndex"),
        "input_value": JsonProperty(str, dump_name="inputValue")
    }
    id = None  # type: int
    argument_index = None  # type: int
    input_type = None  # type: ArgumentType
    input_value = None  # type: str

    @classmethod
    def from_entity(cls, e):
        # type: (DeclarativeInputArgumentItem) -> DeclarativeInputArgumentItemDto
        res = cls(id=e.id, argument_index=e.argument_index, input_type=e.input_type, input_value=e.input_value)
        return res

    @classmethod
    def from_list(cls, list_e):
        # type: (List[DeclarativeInputArgumentItem]) -> List[DeclarativeInputArgumentItemDto]
        res = [DeclarativeInputArgumentItemDto.from_entity(x) for x in list_e]
        return res

    def to_entity(self):
        # type: ()-> DeclarativeInputArgumentItem
        res = DeclarativeInputArgumentItem(self.id, self.argument_index, self.input_type, self.input_value)
        return res
