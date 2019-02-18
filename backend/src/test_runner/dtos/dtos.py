from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from models.question_answer import QuestionAnswer
from models.test_run import TestRun


class TestTemplateDto:
    @staticmethod
    def list_of(test_templates):
        return [TestTemplateDto.from_test(x) for x in test_templates]

    @classmethod
    def from_test(cls, test_template):
        res = cls()
        res.id = test_template.id
        res.name = test_template.name
        res.time_limit = test_template.time_limit
        res.questions = [TestQuestionTemplateDto.from_test(x) for x in test_template.questions]
        return res


class TestQuestionTemplateDto:
    @classmethod
    def from_test(cls, test_template_question):
        res = cls()
        res.id = test_template_question.id
        res.name = test_template_question.name
        res.description = test_template_question.description
        res.time_limit = test_template_question.time_limit
        return res


class CodeRunResult:
    def __init__(self, language, output, output_type, error=None):
        self.language = language
        self.output = output
        self.output_type = output_type
        self.error = error


class TestRunQuestionAnswerDto:
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


class TestRunDto:
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


class TestInstanceUpdate:
    def __init__(self, available_after, disabled_after, time_limit):
        self.available_after = available_after
        self.disabled_after = disabled_after
        self.time_limit = time_limit


class FunctionScaffoldingDto:
    def __init__(self, code, language, function):
        self.function = function
        self.language = language
        self.code = code


class CodeExecutionRequestDto:
    def __init__(self, code, language, is_plain_code, client_id=None, function_id=None, return_type=None):
        # type: (str, LanguageEnum, str, int, ArgumentType) -> None

        self.return_type = return_type  # type: ArgumentType
        self.function_id = function_id  # type: int
        self.language = language  # type: LanguageEnum
        self.code = code  # type: str
        self.is_plain_code = is_plain_code  # type: bool
        self.client_id = client_id  # type: str


class CodeExecutionResponseDto:
    def __init__(self, code_run_result, client_id=None):
        # type: (CodeRunResult, str) -> None

        self.code_run_result = code_run_result
        self.client_id = client_id
