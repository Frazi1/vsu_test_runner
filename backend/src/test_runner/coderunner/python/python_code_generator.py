from typing import List

from coderunner.base_code_generator import BaseCodeGenerator
from coderunner.function_run_argument import FunctionRunArgument
from coderunner.function_run_plan import FunctionRunPlan
from coderunner.scaffolding_type import ScaffoldingType
from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function import Function
from models.function_parameter import FunctionArgument
from shared.value_converter import ValueConverter
from utils.business_error import BusinessException


class PythonCodeGenerator(BaseCodeGenerator):
    _indentation = 4
    _indentation_symbol = " "

    FUNC_DECLARATION_MARKER = "%FUNC_DECLARATION%"
    FUNC_CALL_MARKER = "%FUNC_CALL%"

    def generate_function_call_text(self, function_run_plan: FunctionRunPlan) -> str:
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

    def scaffold_code(self, function_: Function, scaffolding_type: ScaffoldingType) -> str:
        args = [self._translate_parameter(x) for x in function_.arguments]
        res = "def {name}({args}):\n".format(name=function_.name,
                                             args=", ".join(args))
        res += self._get_indent() + self._get_commented_text("Write code here")

        return res

    def _translate_parameter(self, argument: FunctionArgument) -> str:
        return argument.name

    def _get_indent(self) -> str:
        return self._indentation * self._indentation_symbol

    def _get_commented_text(self, text):
        return "# {}".format(text)

    def _indent_line(self, line, last):
        res = " " * self._indentation + line
        if last is not True:
            res += "\n"
        return res

    def _add_fixed_indent(self, code: str, level: int) -> str:
        lines = code.split("\n")
        for index in range(0, len(lines)):
            lines[index] = self._get_indent() * level + lines[index]
        return "\n".join(lines)

    def _add_indent(self, code: str, spaces: int) -> str:
        lines = [x for x in code.split("\n") if x != ""]
        for index in range(0, len(lines)):
            lines[index] = self._indentation_symbol * spaces + lines[index]
        return "\n".join(lines)

    def translate_code(self, function_signature: Function, code_snippet: CodeSnippet) -> str:
        parameters = [self._translate_parameter(x) for x in function_signature.parameters]
        signature = "def {name}({parameters}):\n".format(name=function_signature.name,
                                                         parameters=", ".join(parameters))

        code_lines = code_snippet.code.splitlines()
        formatted_code = "".join(
            [(self._indent_line(x, index == len(code_lines) - 1)) for index, x in enumerate(code_lines)])
        return signature + formatted_code

    def prepare_code_from_template(self, template_text, function_run_plans: List[FunctionRunPlan],
                                   function_declaration_code: str) -> str:
        indent = next(line for line in template_text.split("\n") if self.FUNC_CALL_MARKER in line).index(
            self.FUNC_CALL_MARKER[0])

        function_calls_code = [self.generate_function_call_text(plan) for plan in function_run_plans]
        function_calls_code_indented = [self._add_indent(call_code, indent) for call_code in function_calls_code]
        ready_template = template_text.replace(indent * self._indentation_symbol + self.FUNC_CALL_MARKER,
                                               "\n".join(function_calls_code_indented))

        result_function_declaration = self.add_decorator(function_declaration_code, "__notify_iteration", [])
        result_function_declaration = self._add_indent(result_function_declaration, indent)

        ready_template = ready_template.replace(indent * self._indentation_symbol + self.FUNC_DECLARATION_MARKER,
                                                result_function_declaration)
        return ready_template
