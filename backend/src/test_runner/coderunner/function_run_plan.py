from typing import List

from coderunner.function_run_argument import FunctionRunArgument
from models.function import Function
from models.language_enum import LanguageEnum


class FunctionRunPlan(object):
    def __init__(self, language, code, function_, arguments):
        # type:(LanguageEnum, str, Function, List[FunctionRunArgument]) -> None
        self.code = code  # type: str
        self.language = language  # type: LanguageEnum
        self.arguments = arguments  # type: List[FunctionRunArgument]
        self.function = function_  # type: Function
