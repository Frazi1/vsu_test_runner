from typing import List

from coderunner.function_run_argument import FunctionRunArgument
from models.function import Function


class FunctionRunPlan(object):
    def __init__(self, function_: Function, arguments: List[FunctionRunArgument],
                 expected_result: str,
                 declarative_input_item_id: int) -> None:
        self.arguments = arguments  # type: List[FunctionRunArgument]
        self.function = function_  # type: Function
        self.expected_result = expected_result  # type: str
        self.declarative_input_item_id = declarative_input_item_id
