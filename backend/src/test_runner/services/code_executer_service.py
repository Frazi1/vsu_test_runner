from typing import List, Optional

from coderunner.base_runner import BaseRunner
from coderunner.execution_type import ExecutionType
from coderunner.file_run_result import FileRunResult
from coderunner.function_run_plan import FunctionRunPlan
from dtos.dtos import FunctionScaffoldingDto, CodeExecutionRequestDto
from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function import Function
from models.language_enum import LanguageEnum
from services.function_service import FunctionService
from services.models.code_run_result import CodeRunResult
from services.models.code_run_validation_result import CodeRunValidationResult
from shared.value_converter import ValueConverter
from utils.business_error import BusinessException


class CodeExecuterService:
    def __init__(self,
                 function_service  # type: FunctionService
                 ):
        self._function_service = function_service

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

    def scaffold_function(self, function_id, language):
        # type: (int, LanguageEnum) -> FunctionScaffoldingDto

        func = self._function_service.get_function_by_id(function_id)
        runner = self._find_runner(language)
        code = runner.code_generator.scaffold_function_declaration_text(func)
        return FunctionScaffoldingDto(code, language, func)

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

        if code_execution_request.execution_type == ExecutionType.PLAIN_TEXT:
            run_results = runner.execute_plain_code(code_execution_request.code, testing_inputs)
        elif code_execution_request.execution_type == ExecutionType.ONE_BY_ONE:
            run_results = self.execute_tests_one_by_one(code_execution_request.language,
                                                        code_execution_request.code,
                                                        testing_inputs,
                                                        return_type)
        else:
            raise NotImplementedError("Comprehensive function execution is not implemented yet!")
        return [CodeRunResult(result, plan) for result, plan in
                (zip(run_results, run_plans or [None] * len(run_results)))]

    def _execute_plans_for_valid_results(self, code_execution_request: CodeExecutionRequestDto,
                                         plans: List[FunctionRunPlan]) -> None:
        execution_results = self.execute_code(code_execution_request, plans)
        for result in execution_results:
            plan = result.run_plan
            if plan.expected_result is not None and plan.expected_result != "": continue
            plan.expected_result = result.file_run_result.output

    def run_testing_set(self, code_snippet: CodeSnippet, function_: Function) -> List[CodeRunValidationResult]:
        plans = self._function_service.get_function_run_plans(function_.id)
        code_execution_request_for_valid_results = CodeExecutionRequestDto(function_.code_snippets[0].code,
                                                                           code_snippet.language,
                                                                           ExecutionType.ONE_BY_ONE,
                                                                           function_.id,
                                                                           function_.return_type,
                                                                           client_id=None)
        self._execute_plans_for_valid_results(code_execution_request_for_valid_results, plans)

        code_execution_request = CodeExecutionRequestDto(code_snippet.code,
                                                         code_snippet.language,
                                                         ExecutionType.ONE_BY_ONE,
                                                         function_.id,
                                                         function_.return_type,
                                                         client_id=None)
        results = self.execute_code(code_execution_request, plans)
        return self.validate_results(results)

    def validate_results(self, code_run_results: List[CodeRunResult]) -> List[CodeRunValidationResult]:
        res = []
        for run_result in code_run_results:
            is_valid = not run_result.file_run_result.error and run_result.file_run_result.output == run_result.run_plan.expected_result
            res.append(CodeRunValidationResult(run_result, is_valid))
        return res

    def execute_tests_one_by_one(self,
                                 language: LanguageEnum,
                                 code: str,
                                 inputs: List[str],
                                 return_type: ArgumentType) -> List[FileRunResult]:
        runner = self._find_runner(language)
        outputs = runner.execute_plain_code(code, inputs)
        return outputs

    def _generate_input_from_plan(self, plan: FunctionRunPlan) -> str:
        res = ""
        for arg in plan.arguments:
            parsed_value = ValueConverter.from_string(arg.argument_type, arg.argument_value)
            if arg.argument_type == ArgumentType.INTEGER or arg.argument_type == ArgumentType.STRING:
                res += str(arg.argument_value)
            elif arg.argument_type == ArgumentType.ARRAY_INTEGER or arg.argument_type == ArgumentType.ARRAY_STRING:
                res += ", ".join([str(x) for x in parsed_value])

        return res
