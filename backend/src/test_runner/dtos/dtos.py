from datetime import datetime
from typing import List

from coderunner.execution_type import ExecutionType
from coderunner.scaffolding_type import ScaffoldingType
from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function import Function
from models.function_inputs.base_function_input import DeclarativeFunctionInput, BaseFunctionInput
from models.function_inputs.code_run_iteration import CodeRunIteration
from models.function_inputs.declarative_input_argument_item import DeclarativeInputArgumentItem
from models.function_inputs.declarative_input_item import DeclarativeInputItem
from models.function_parameter import FunctionArgument
from models.language_enum import LanguageEnum
from models.question_answer import QuestionAnswer
from models.test_question_template import TestQuestionTemplate
from models.test_run import TestRun
from models.test_template import TestTemplate
from utils.helpers import is_relationship_loaded
from utils.pyjson.pyjson import BaseJsonable, JsonProperty


class BaseDto(BaseJsonable):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
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
        "is_deleted": JsonProperty(bool, dump_name='isDeleted', required=False),
        "version": JsonProperty(int, required=False),
        "time_limit": JsonProperty(int, dump_name='timeLimit', required=False),
        "description": JsonProperty(str),
        "id": JsonProperty(int, required=False),
        "solution_code_snippet": JsonProperty("CodeSnippetDto", dump_name='codeSnippet'),
        "name": JsonProperty(str)
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
        "questions": JsonProperty([TestQuestionTemplateDto], dump_name="questionTemplates"),
        "is_deleted": JsonProperty(bool, dump_name="isDeleted", required=False),
        "time_limit": JsonProperty(int, dump_name="timeLimit", required=False),
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
        res = cls(id=e.id,
                  name=e.name,
                  time_limit=e.time_limit,
                  questions=TestQuestionTemplateDto.from_list(e.questions),
                  is_deleted=e.is_deleted)
        return res

    def to_entity(self):
        return TestTemplate(self.id, self.name, self.time_limit, [x.to_entity() for x in self.questions])


class CodeRunResultDto(object):
    __exportables__ = {
        "language": JsonProperty(LanguageEnum),
        "output": JsonProperty(str),
        "input": JsonProperty(str),
        "output_type": JsonProperty(ArgumentType, "outputType"),
        "error": JsonProperty(str)
    }

    def __init__(self, language, input: str, output, output_type, error=None):
        self.input = input
        self.language = language
        self.output = output
        self.output_type = output_type
        self.error = error


class CodeRunIterationDto(BaseJsonable):
    __exportables__ = {
        "actual_output": JsonProperty(str, "actualOutput"),
        "expected_output": JsonProperty(str, "expectedOutput", required=False)
    }
    actual_output: str = None
    expected_output: str = None

    def __init__(self, actual_output: str = None, expected_output: str = None):
        self.actual_output = actual_output
        self.expected_output = expected_output

    @classmethod
    def from_entity(cls, code_run_iteration: CodeRunIteration) -> "CodeRunIterationDto":
        return CodeRunIterationDto(actual_output=code_run_iteration.actual_output,
                                   expected_output=code_run_iteration.iteration_template.output_value)

    @classmethod
    def from_entity_list(cls, entities: List[CodeRunIteration]) -> List["CodeRunIterationDto"]:
        return [CodeRunIterationDto.from_entity(x) for x in entities]


class QuestionAnswerDto(BaseJsonable):
    __exportables__ = {
        "id": JsonProperty(int),
        "name": JsonProperty(str),
        "description": JsonProperty(str),
        "answer_code_snippet": JsonProperty("CodeSnippetDto", dump_name="answerCodeSnippet", required=False),
        "function_id": JsonProperty(int, dump_name="functionId"),
        "is_validated": JsonProperty(bool, "isValidated"),
        "validation_passed": JsonProperty(bool, "validationPassed", required=False),
        "iterations": JsonProperty([CodeRunIterationDto])
    }

    def __init__(self, id=None, name=None, description=None, answer_code_snippet=None, function_id=None,
                 is_validated=None, validation_passed=None, iterations: List[CodeRunIterationDto] = None):
        self.id = id  # type:int
        self.name = name  # type:str
        self.description = description  # type:str
        self.answer_code_snippet = answer_code_snippet  # type:CodeSnippetDto
        self.function_id = function_id  # type:int
        self.validation_passed = validation_passed  # type: bool
        self.is_validated = is_validated  # type: bool
        self.iterations = iterations

    @classmethod
    def map_from(cls, question_answer):
        # type: (QuestionAnswer) -> QuestionAnswerDto
        cls_ = cls(id=question_answer.id,
                   name=question_answer.question_instance.name,
                   description=question_answer.question_instance.description,
                   answer_code_snippet=CodeSnippetDto.from_entity(
                       question_answer.code_snippet) if question_answer.code_snippet is not None else None,
                   function_id=question_answer.question_instance.solution_code_snippet.function_id,
                   validation_passed=question_answer.validation_passed,
                   is_validated=question_answer.is_validated,
                   iterations=CodeRunIterationDto.from_entity_list(question_answer.answer_iteration_results))
        return cls_


class TestRunDto(BaseJsonable):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "name": JsonProperty(str),
        "started_at": JsonProperty(datetime, dump_name="startedAt"),
        "ends_at": JsonProperty(datetime, dump_name="endsAt", required=False),
        "finished_at": JsonProperty(datetime, dump_name="finishedAt", required=False),
        "time_limit": JsonProperty(int, dump_name="timeLimit", required=False),
        "question_answers": JsonProperty([QuestionAnswerDto], dump_name="questionAnswers")
    }

    def __init__(self, id=None, name=None, started_at=None, ends_at=None, finished_at=None, time_limit=None,
                 question_answers=None):
        self.id = id  # type: int
        self.name = name  # type: str
        self.started_at = started_at  # type: datetime
        self.ends_at = ends_at  # type: datetime
        self.finished_at = finished_at  # type: datetime
        self.time_limit = time_limit  # type: int
        self.question_answers = question_answers  # type: List[QuestionAnswerDto]

    @classmethod
    def from_entity(cls, test_run):
        # type: (TestRun) -> TestRunDto
        cls_ = cls(id=test_run.id,
                   name=test_run.test_instance.name,
                   started_at=test_run.started_at,
                   ends_at=test_run.ends_at,
                   finished_at=test_run.finished_at,
                   time_limit=test_run.test_instance.time_limit,
                   question_answers=[QuestionAnswerDto.map_from(x) for x in test_run.question_answers])
        return cls_

    @classmethod
    def from_entity_list(cls, test_runs):
        # type:(List[TestRun])->List[TestRunDto]
        return [TestRunDto.from_entity(e) for e in test_runs]


class TestRunAnswerUpdateDto(BaseJsonable):
    __exportables__ = {
        "answer_id": JsonProperty(int, dump_name="answerId"),
        "answer_code_snippet": JsonProperty("CodeSnippetDto", dump_name="answerCodeSnippet")
    }
    answer_id = None  # type: int
    answer_code_snippet = None  # type: CodeSnippetDto


class TestInstanceUpdate(object):
    def __init__(self, available_after, disabled_after, time_limit):
        self.available_after = available_after
        self.disabled_after = disabled_after
        self.time_limit = time_limit


class FunctionScaffoldingDto(BaseJsonable):
    __exportables__ = {
        # "function": JsonProperty(Function),
        "language":JsonProperty(LanguageEnum),
        "code": JsonProperty(str),
        "scaffolding_type":JsonProperty(ScaffoldingType, "scaffoldingType")
    }

    def __init__(self, code: str, language: LanguageEnum, function: Function, scaffolding_type:ScaffoldingType):
        self.function = function
        self.language = language
        self.code = code
        self.scaffolding_type = scaffolding_type


class CodeExecutionRequestDto(BaseJsonable):
    __exportables__ = {
        "return_type": JsonProperty(ArgumentType, "returnType"),
        "function_id": JsonProperty(int, "functionId", required=False),
        "language": JsonProperty(LanguageEnum),
        "code": JsonProperty(str),
        "scaffolding_type": JsonProperty(ScaffoldingType, "scaffoldingType"),
        "client_id": JsonProperty(str, "clientId", required=False)
    }

    def __init__(self, code: str = '', language: LanguageEnum = None, scaffolding_type: ScaffoldingType = None,
                 function_id: int = None, return_type: ArgumentType = None, client_id: str = None):
        self.return_type = return_type
        self.function_id = function_id
        self.language = language
        self.code = code
        self.scaffolding_type = scaffolding_type
        self.client_id = client_id


class CodeExecutionResponseDto(BaseDto):
    __exportables__ = {
        "is_valid": JsonProperty(bool, "isValid", required=False),
        "actual_input": JsonProperty(str, "actualInput", required=False),
        "actual_output": JsonProperty(str, "actualOutput")
    }

    def __init__(self, actual_input: str, actual_output: str, is_valid: bool = None, **kwargs):
        super().__init__(**kwargs)
        self.actual_input = actual_input
        self.actual_output = actual_output
        self.is_valid = is_valid


class CreateFunctionTestingInputRequestDto(object):
    def __init__(self, function_id, declarative_input):
        # type: (int, DeclarativeFunctionInput) -> None
        self.function_id = function_id
        self.declarative_input = declarative_input


class CodeSnippetDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "function": JsonProperty("FunctionDto", required=False),
        "code": JsonProperty(str, required=False),
        "language": JsonProperty(LanguageEnum)
    }

    id = None  # type: int
    function = None  # type: FunctionDto
    code = None  # type: str
    language = None  # type: LanguageEnum

    @classmethod
    def from_entity(cls, e):
        # type: (CodeSnippet) -> CodeSnippetDto
        if is_relationship_loaded(e, CodeSnippet.function) and e.function:
            function_dto = FunctionDto.from_entity(e.function)
        else:
            function_dto = None
        res = cls(id=e.id, language=e.language, code=e.code,
                  function=function_dto
                  )
        return res

    def to_entity(self):
        res = CodeSnippet(id=self.id, language=self.language, code=self.code, function=self.function.to_entity())
        return res


class FunctionDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "return_type": JsonProperty(ArgumentType, dump_name="returnType"),
        "name": JsonProperty(str),
        "arguments": JsonProperty(["FunctionArgumentDto"]),
        "testing_input": JsonProperty("FunctionInputDto", dump_name="testingInput", required=False)
    }
    testing_input = None
    arguments = None  # type: List[FunctionArgumentDto]
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
    def from_entity(cls, function):
        # type: (Function) -> FunctionDto
        function_input_dto = FunctionInputDto.from_entity(function.testing_input) \
            if is_relationship_loaded(function, Function.testing_input) else None

        res = cls.create(function.id,
                         function.name,
                         function.return_type,
                         FunctionArgumentDto.list_of(function.arguments),
                         function_input_dto)
        return res

    def to_entity(self):
        res = Function(self.id, self.name, self.return_type, [x.to_entity() for x in self.arguments],
                       self.testing_input.to_entity() if self.testing_input else None)
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
        return FunctionArgument(id=self.id, type=self.type, name=self.name)


class FunctionInputDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "declarative_input": JsonProperty("DeclarativeFunctionInputDto", dump_name="declarativeInput", required=False)
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
        res = cls(items=[DeclarativeInputItemDto.from_entity(x) for x in e.items])
        return res


class DeclarativeInputItemDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int, required=False),
        "declarative_argument_item_dtos": JsonProperty(["DeclarativeInputArgumentItemDto"], dump_name="argumentItems"),
        "output_value": JsonProperty(str, dump_name="outputValue", required=False)
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
        "input_type": JsonProperty(ArgumentType, dump_name="inputType"),
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


class FinishedTestRunResultsDto(BaseDto):
    __exportables__ = {
        "id": JsonProperty(int),
        "answer_results": JsonProperty([QuestionAnswerDto]),
        "finished_at": JsonProperty(datetime, "finishedAt")
    }

    id = None  # type: int
    name = None  # type: str
    answer_results = None  # type: List[QuestionAnswerDto]
    finished_at = None  # type: datetime
