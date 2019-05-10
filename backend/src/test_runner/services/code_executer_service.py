from typing import List, Optional

from coderunner.base_runner import BaseRunner
from coderunner.execution_type import ExecutionType
from coderunner.file_run_result import FileRunResult
from coderunner.function_run_plan import FunctionRunPlan
from coderunner.scaffolding_type import ScaffoldingType
from dtos.dtos import FunctionScaffoldingDto, CodeExecutionRequestDto, FunctionInputDto
from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function import Function
from models.language_enum import LanguageEnum
from services.base_service import BaseService
from services.function_service import FunctionService
from services.models.code_run_result import CodeRunResult
from services.models.code_run_validation_result import CodeRunValidationResult
from services.testing_input_service import TestingInputService
from shared.value_converter import ValueConverter
from utils.business_error import BusinessException
from utils.run_plan_helpers import get_run_plans
import utils.validation_utils as validation


class CodeExecuterService(BaseService):
    def __init__(self,
                 function_service: FunctionService,
                 testing_input_service: TestingInputService,
                 ):
        self._function_service = function_service
        self._testing_input_service = testing_input_service

    _runners = {}

    def register_runner(self, cls_):
        print("TYPE: {}".format(type(cls_)))
        try:
            languages = [cls_.supported_language]
            for lang in languages:
                if lang not in self._runners:
                    print("REGISTER:{}, language:{}".format(cls_, lang))
                    self._runners[lang] = cls_
        except Exception as e:
            print(e)

    def _find_runner(self, language):
        # type: (LanguageEnum) -> BaseRunner

        return self._runners[language]

    def get_supported_languages(self):
        return self._runners.keys()

    def scaffold_function(self, function_id: int, language: LanguageEnum,
                          scaffolding_type: ScaffoldingType) -> FunctionScaffoldingDto:

        func = self._function_service.get_function_by_id(function_id)
        runner = self._find_runner(language)
        code = runner.code_generator.scaffold_code(func, scaffolding_type)
        return FunctionScaffoldingDto(code, language, func, scaffolding_type)

    def execute_code_with_request_testing_input(self, code_execution_request: CodeExecutionRequestDto) -> List[
        CodeRunResult]:
        validation.is_not_none(code_execution_request.testing_input, "code_execution_request.testing_input")
        validation.is_not_none(code_execution_request.testing_input.declarative_input,
                               "code_execution_request.testing_input.declarative_input")

        run_plans = get_run_plans(
            function_=None,
            testing_input=FunctionInputDto.to_entity(code_execution_request.testing_input)
        )
        return self.execute_code(code_execution_request, run_plans)

    def execute_code(self, code_execution_request: CodeExecutionRequestDto,
                     run_plans: Optional[List[FunctionRunPlan]]) -> List[CodeRunResult]:

        function_ = self._function_service.get_function_by_id(code_execution_request.function_id)

        if code_execution_request.return_type:
            return_type = code_execution_request.return_type
        elif code_execution_request.function_id:
            return_type = function_.return_type
        else:
            raise BusinessException("Return type or Function ID must be specified")

        runner = self._find_runner(code_execution_request.language)
        testing_inputs = [self._generate_input_from_plan(plan) for plan in run_plans] if run_plans else [None]

        code_for_execution = code_execution_request.code
        if code_execution_request.scaffolding_type == ScaffoldingType.FUNCTION_ONLY:
            code_for_execution = runner.code_generator.prepare_execution_code_from_function_declaration(
                code_for_execution, function_)

        run_results = runner.execute_plain_code(code_for_execution, testing_inputs)

        return [CodeRunResult(result, plan) for result, plan in
                (zip(run_results, run_plans or [None] * len(run_results)))]

    def _execute_plans_for_valid_results(self, code_execution_request: CodeExecutionRequestDto,
                                         plans: List[FunctionRunPlan]) -> None:
        execution_results = self.execute_code(code_execution_request, plans)
        for result in execution_results:
            plan = result.run_plan
            if plan.expected_result is not None and plan.expected_result != "": continue
            plan.expected_result = result.file_run_result.output

    def execute_function_tests_and_save_valid_results(self, code_snippet: CodeSnippet,
                                                      function_: Function,
                                                      function_run_plans: List[FunctionRunPlan]) -> None:
        code_execution_request_for_valid_results = CodeExecutionRequestDto(function_.code_snippets[0].code,
                                                                           code_snippet.language,
                                                                           ScaffoldingType.FULL_TEMPLATE,
                                                                           function_.id,
                                                                           function_.return_type,
                                                                           client_id=None)
        self._execute_plans_for_valid_results(code_execution_request_for_valid_results, function_run_plans)
        self._testing_input_service.update_testing_input(function_run_plans)

    def run_testing_set(self, code_snippet: CodeSnippet, function_: Function) -> List[CodeRunValidationResult]:
        plans = self._function_service.get_function_run_plans(function_.id)
        code_execution_request_for_valid_results = CodeExecutionRequestDto(function_.code_snippets[0].code,
                                                                           code_snippet.language,
                                                                           ScaffoldingType.FULL_TEMPLATE,
                                                                           function_.id,
                                                                           function_.return_type,
                                                                           client_id=None)
        self._execute_plans_for_valid_results(code_execution_request_for_valid_results, plans)

        code_execution_request = CodeExecutionRequestDto(code_snippet.code,
                                                         code_snippet.language,
                                                         ScaffoldingType.FUNCTION_ONLY,
                                                         function_.id,
                                                         function_.return_type,
                                                         client_id=None)
        results = self.execute_code(code_execution_request, plans)
        return self.validate_results(results)

    def validate_results(self, code_run_results: List[CodeRunResult]) -> List[CodeRunValidationResult]:
        res = []
        for run_result in code_run_results:
            if run_result.file_run_result.error:
                is_valid = False
            else:
                is_valid = run_result.file_run_result.output == run_result.run_plan.expected_result
            res.append(CodeRunValidationResult(run_result, is_valid))
        return res

    def _generate_input_from_plan(self, plan: FunctionRunPlan) -> str:
        res = ""
        for arg in plan.arguments:
            parsed_value = ValueConverter.from_string(arg.argument_type, arg.argument_value, parse_str=False)
            if arg.argument_type == ArgumentType.INTEGER or arg.argument_type == ArgumentType.STRING:
                res += str(parsed_value)
            elif arg.argument_type == ArgumentType.ARRAY_INTEGER or arg.argument_type == ArgumentType.ARRAY_STRING:
                res += ", ".join([str(x) for x in parsed_value])

        return res
