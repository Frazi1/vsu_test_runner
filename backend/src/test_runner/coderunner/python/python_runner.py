import os

from app_config import Config
from coderunner.function_run_plan import FunctionRunPlan
from coderunner.python.python_code_generator import PythonCodeGenerator
from coderunner.simple_runner import SimpleRunner
from dtos.dtos import CodeRunResult
from models.argument_type import ArgumentType
from models.function import Function
from models.function_parameter import FunctionArgument
from models.language_enum import LanguageEnum


class PythonRunner(SimpleRunner):
    __file_ext__ = ".py"
    _indentation = 4
    _indentation_symbol = " "

    supported_languages = [LanguageEnum.PYTHON]
    code_generator = PythonCodeGenerator()

    def __init__(self, config):
        # type: (Config) -> None
        super(PythonRunner, self).__init__(config)

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

    def translate_code(self, function_signature, code_snippet):
        parameters = [self._translate_parameter(x) for x in function_signature.parameters]
        signature = "def {name}({parameters}):\n".format(name=function_signature.name,
                                                         parameters=", ".join(parameters))

        code_lines = code_snippet.code.splitlines()
        formatted_code = "".join(
            [(self._indent_line(x, index == len(code_lines) - 1)) for index, x in enumerate(code_lines)])
        return signature + formatted_code

    def execute_plain_code(self, return_type, code):
        # type: (ArgumentType, str) -> CodeRunResult

        file_path = self.save_code_to_file(None, self.__file_ext__, code)
        try:
            result = self.run_file("python", self.supported_languages[0], file_path, return_type)
        finally:
            os.remove(file_path)
        return result

    def execute_default_template(self, function_run_plan):
        # type: (FunctionRunPlan) -> CodeRunResult
        with open(self._config.python_default_template_path, "r") as file_:
            template_text = file_.read()

        ready_template = template_text \
            .replace("%FUNC_CALL%", self.code_generator.generate_function_call_text(function_run_plan) + "\n") \
            .replace("%FUNC_DECLARATION%", function_run_plan.code + "\n")

        return self.execute_plain_code(function_run_plan.function.return_type, ready_template)

    def scaffold_function_declaration_text(self, function_):
        # type: (Function, LanguageEnum) -> str

        args = [self._translate_parameter(x) for x in function_.arguments]
        res = "def {name}({args}):\n".format(name=function_.name,
                                             args=", ".join(args))
        res += self._get_indent() + self._get_commented_text("Write code here")

        return res
