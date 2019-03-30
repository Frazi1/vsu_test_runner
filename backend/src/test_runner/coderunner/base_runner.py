from abc import abstractmethod
from typing import List

from coderunner.base_code_generator import BaseCodeGenerator
from coderunner.file_run_result import FileRunResult
from coderunner.function_run_plan import FunctionRunPlan
from dtos.dtos import CodeRunResultDto


class BaseRunner(object):
    def __init__(self, code_generator: BaseCodeGenerator):
        self.code_generator = code_generator

    @property
    @abstractmethod
    def supported_language(self):
        pass

    @abstractmethod
    def execute_plain_code(self, code: str, inputs: List[str]) -> List[FileRunResult]:
        pass

    @abstractmethod
    def execute_default_template(self,
                                 function_declaration_code: str,
                                 function_run_plans: List[FunctionRunPlan]) -> List[CodeRunResultDto]:
        pass
