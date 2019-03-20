from abc import abstractmethod
from typing import List

from coderunner.base_code_generator import BaseCodeGenerator
from coderunner.function_run_plan import FunctionRunPlan
from dtos.dtos import CodeRunResult
from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function import Function


class BaseRunner(object):
    def __init__(self, code_generator: BaseCodeGenerator):
        self.code_generator = code_generator

    @property
    @abstractmethod
    def supported_language(self):
        pass

    def execute_snippet(self, function_signature: Function, code_snippet: CodeSnippet) -> List[CodeRunResult]:
        code = self.code_generator.translate_code(function_signature, code_snippet)
        return self.execute_plain_code(function_signature.return_type, code)

    @abstractmethod
    def execute_plain_code(self, return_type: ArgumentType, code: str) -> List[CodeRunResult]:
        pass

    @abstractmethod
    def execute_default_template(self,
                                 function_declaration_code: str,
                                 function_run_plans: List[FunctionRunPlan]) -> List[CodeRunResult]:
        pass
