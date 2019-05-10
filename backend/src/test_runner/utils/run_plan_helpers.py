from typing import List, Optional

from coderunner.function_run_argument import FunctionRunArgument
from coderunner.function_run_plan import FunctionRunPlan
from models.function import Function
from models.function_inputs.base_function_input import DeclarativeFunctionInput, BaseFunctionInput
from shared.value_converter import ValueConverter


def get_run_plans(function_: Optional[Function], testing_input: BaseFunctionInput) -> Optional[List[FunctionRunPlan]]:
    if testing_input is None:
        return None
    if isinstance(testing_input, DeclarativeFunctionInput):
        res = [FunctionRunPlan(function_,
                               [
                                   FunctionRunArgument(arg.input_type, arg.input_value) for arg in
                                   input.argument_items
                               ],
                               input.output_value,
                               input.id)
               for input in testing_input.items]
        return res
    raise NotImplementedError("Input type {} is not supported".format(testing_input.type))
