import os
import re
from typing import List

from app_config import Config
from coderunner.function_run_plan import FunctionRunPlan
from coderunner.python.python_code_generator import PythonCodeGenerator
from coderunner.simple_runner import SimpleRunner
from dtos.dtos import CodeRunResult
from models.argument_type import ArgumentType
from models.function import Function
from models.function_parameter import FunctionArgument
from models.language_enum import LanguageEnum
from shared.value_converter import ValueConverter


class PythonRunner(SimpleRunner):
    __file_ext__ = ".py"
    _indentation = 4
    _indentation_symbol = " "

    @property
    def supported_language(self):
        return LanguageEnum.PYTHON

    code_generator = PythonCodeGenerator()

    def __init__(self, config):
        # type: (Config) -> None
        super(PythonRunner, self).__init__(config)
        self.FUNC_DECLARATION_MARKER = "%FUNC_DECLARATION%"
        self.FUNC_CALL_MARKER = "%FUNC_CALL%"

    def _translate_parameter(self, argument):
        # type: (FunctionArgument) -> str
        return argument.name

    def _get_indent(self):
        # type: () -> str
        return self._indentation * self._indentation_symbol

    def _get_commented_text(self, text):
        return "# {}".format(text)

    def _indent_line(self, line, last):
        res = " " * self._indentation + line
        if last is not True:
            res += "\n"
        return res

    def _add_fixed_indent(self, code, level):
        # type:(str, int) -> str
        lines = code.split("\n")
        for index in range(0, len(lines)):
            lines[index] = self._get_indent() * level + lines[index]
        return "\n".join(lines)

    def _add_indent(self, code: str, spaces: int) -> str:
        lines = [x for x in code.split("\n") if x != ""]
        for index in range(0, len(lines)):
            lines[index] = self._indentation_symbol * spaces + lines[index]
        return "\n".join(lines)

    def translate_code(self, function_signature, code_snippet):
        parameters = [self._translate_parameter(x) for x in function_signature.parameters]
        signature = "def {name}({parameters}):\n".format(name=function_signature.name,
                                                         parameters=", ".join(parameters))

        code_lines = code_snippet.code.splitlines()
        formatted_code = "".join(
            [(self._indent_line(x, index == len(code_lines) - 1)) for index, x in enumerate(code_lines)])
        return signature + formatted_code

    def _parse_out_file(self, out: str, language: LanguageEnum, return_type: ArgumentType) -> List[CodeRunResult]:
        regex = re.compile(
            r'<StartIteration>{line_splitter}(.*?){line_splitter}<EndIteration>'.format(line_splitter=os.linesep),
            re.RegexFlag.MULTILINE | re.RegexFlag.DOTALL)
        raw_results = regex.findall(out)
        typed_results = [CodeRunResult(language,
                                       ValueConverter.to_string(return_type,
                                                                ValueConverter.from_string(return_type, res,
                                                                                           parse_str=False)),
                                       return_type) for res in raw_results]
        return typed_results

    def execute_plain_code(self, return_type: ArgumentType, code: str) -> List[CodeRunResult]:
        file_path = self.save_code_to_file(None, self.__file_ext__, code)
        try:
            result = self.run_file("python", file_path)
            typed_results = self._parse_out_file(result, self.supported_language, return_type)
        finally:
            os.remove(file_path)

        return typed_results

    def execute_default_template(self,
                                 function_declaration_code: str,
                                 function_run_plans: List[FunctionRunPlan]) -> List[CodeRunResult]:
        with open(self._config.python_default_template_path, "r") as file_:
            template_text = file_.read()

        indent = next(line for line in template_text.split("\n") if self.FUNC_CALL_MARKER in line).index(
            self.FUNC_CALL_MARKER[0])

        function_calls_code = [self.code_generator.generate_function_call_text(plan) for plan in function_run_plans]
        function_calls_code_indented = [self._add_indent(call_code, indent) for call_code in function_calls_code]
        ready_template = template_text.replace(indent * self._indentation_symbol + self.FUNC_CALL_MARKER,
                                               "\n".join(function_calls_code_indented))

        result_function_declaration = self.code_generator.add_decorator(function_declaration_code,
                                                                        "__notify_iteration", [])
        result_function_declaration = self._add_indent(result_function_declaration, indent)

        ready_template = ready_template.replace(indent * self._indentation_symbol + self.FUNC_DECLARATION_MARKER,
                                                result_function_declaration)

        return self.execute_plain_code(function_run_plans[0].function.return_type, ready_template)

    def scaffold_function_declaration_text(self, function_: Function) -> str:
        args = [self._translate_parameter(x) for x in function_.arguments]
        res = "def {name}({args}):\n".format(name=function_.name,
                                             args=", ".join(args))
        res += self._get_indent() + self._get_commented_text("Write code here")

        return res
