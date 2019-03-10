from coderunner.function_run_argument import FunctionRunArgument
from coderunner.function_run_plan import FunctionRunPlan
from models.argument_type import ArgumentType
from shared.value_converter import ValueConverter


class PythonCodeGenerator():
    def generate_function_call_text(self, function_run_plan):
        # type: (FunctionRunPlan) -> str
        return "res = {func}({args})\n".format(func=function_run_plan.function.name,
                                         args=", ".join([self.generate_type_value_repr_text(x) for x in
                                                         function_run_plan.arguments]))

    def generate_type_value_repr_text(self, function_run_argument):
        # type:(FunctionRunArgument) -> str
        argument_type = function_run_argument.argument_type
        argument_value = function_run_argument.argument_value
        if argument_type == ArgumentType.STRING:
            return '"{}"'.format(function_run_argument.argument_value)
        elif argument_type == ArgumentType.INTEGER:
            return function_run_argument.argument_value
        elif argument_type == ArgumentType.ARRAY_INTEGER:
            return '[{values}]'.format(
                values=", ".join(ValueConverter.from_string(argument_type, argument_value)))
        elif argument_type == ArgumentType.ARRAY_STRING:
            res = '[{values}]'
            values = ['"{x}"'.format(x=x) for x in ValueConverter.from_string(argument_type, argument_value)]
            return res.format(values=values)
        else:
            raise NotImplementedError("Type '{}' support is not implemented".format(argument_type))
