from typing import List

from coderunner.function_run_argument import FunctionRunArgument
from models.function import Function
from models.language_enum import LanguageEnum


class FunctionRunPlan(object):
    def __init__(self, language: LanguageEnum, function_: Function, arguments: List[FunctionRunArgument],
                 expected_result: str) -> None:
        self.language = language  # type: LanguageEnum
        self.arguments = arguments  # type: List[FunctionRunArgument]
        self.function = function_  # type: Function
        self.expected_result = expected_result  # type: str
