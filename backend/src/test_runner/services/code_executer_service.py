from typing import List

from coderunner.base_runner import BaseRunner
from coderunner.execution_type import ExecutionType
from coderunner.function_run_plan import FunctionRunPlan
from dtos.dtos import FunctionScaffoldingDto, CodeRunResult, CodeExecutionRequestDto
from models.code_snippet import CodeSnippet
from models.function import Function
from models.language_enum import LanguageEnum
from services.function_service import FunctionService
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
            languages = cls_.supported_languages
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

    def execute_snippet(self, function_signature, code_snippet):
        runner = self._find_runner(code_snippet.language)
        return runner.execute_snippet(function_signature, code_snippet)

    def execute_code(self, code_execution_request):
        # type: (CodeExecutionRequestDto) -> CodeRunResult

        function_ = self._function_service.get_function_by_id(code_execution_request.function_id)

        if code_execution_request.return_type:
            return_type = code_execution_request.return_type
        elif code_execution_request.function_id:
            return_type = function_.return_type
        else:
            raise BusinessException("Return type or Function ID must be specified")

        runner = self._find_runner(code_execution_request.language)
        if code_execution_request.execution_type == ExecutionType.PLAIN_TEXT:
            return runner.execute_plain_code(return_type,
                                             code_execution_request.code)
        else:
            raise NotImplementedError("Comprehensive function execution is not implemented yet!")

    def scaffold_function(self, function_id, language):
        # type: (int, LanguageEnum) -> FunctionScaffoldingDto

        func = self._function_service.get_function_by_id(function_id)
        runner = self._find_runner(language)
        code = runner.scaffold_function_declaration_text(func)
        return FunctionScaffoldingDto(code, language, func)

    def run_testing_set(self, code_snippet, function_):
        # type: (CodeSnippet, Function) -> List[(bool,CodeRunResult)]
        plans = self._function_service.get_function_run_plans(function_.id, code_snippet.code, code_snippet.language)
        runner = self._find_runner(code_snippet.language)
        results = [runner.execute_default_template(plan) for plan in plans]
        validation_results = self.validate_results(results, plans)
        return validation_results

    def validate_results(self, code_execution_results, plans):
        # type: (List[CodeRunResult], List[FunctionRunPlan]) -> (bool, CodeRunResult)
        res = []
        for index in range(0, len(code_execution_results)):
            if not code_execution_results[index].error and \
                    code_execution_results[index].output == plans[index].expected_result:
                res.append((True, code_execution_results[index]))
            else:
                res.append((False, code_execution_results[index]))
        return res
