from typing import List

from coderunner.function_run_argument import FunctionRunArgument
from coderunner.function_run_plan import FunctionRunPlan
from models.argument_type import ArgumentType
from shared.value_converter import ValueConverter
from utils.business_error import BusinessException


class PythonCodeGenerator():
    def generate_function_call_text(self, function_run_plan):
        # type: (FunctionRunPlan) -> str
        arguments_ = [self.generate_type_value_repr_text(x) for x in function_run_plan.arguments]
        return "res = " + self._generate_function_call_inner(function_run_plan.function.name, arguments_)

    def _generate_function_call_inner(self, function_name: str, raw_argument_values: List[str]) -> str:
        return "{func}({args})\n".format(func=function_name, args=", ".join(raw_argument_values))

    def generate_type_value_repr_text(self, function_run_argument: FunctionRunArgument) -> str:
        argument_type = function_run_argument.argument_type
        argument_value = function_run_argument.argument_value
        if argument_type == ArgumentType.STRING:
            return '"{}"'.format(function_run_argument.argument_value)
        elif argument_type == ArgumentType.INTEGER:
            return function_run_argument.argument_value
        elif argument_type == ArgumentType.ARRAY_INTEGER:
            res = '[{values}]'
            return res.format(
                values=", ".join([str(x) for x in (ValueConverter.from_string(argument_type, argument_value))]))
        elif argument_type == ArgumentType.ARRAY_STRING:
            res = '{values}'
            values = ['{x}'.format(x=x) for x in ValueConverter.from_string(argument_type, argument_value)]
            return res.format(values=values)
        else:
            raise NotImplementedError("Type '{}' support is not implemented".format(argument_type))

    def add_decorator(self, func_declaration_code: str, decorator_name: str, decorator_params: List[str]):
        if not func_declaration_code.startswith("def"):
            raise BusinessException("Function declaration should start with 'def'")
        decorator_call = self._generate_function_call_inner("@" + decorator_name, decorator_params)
        return decorator_call + func_declaration_code
