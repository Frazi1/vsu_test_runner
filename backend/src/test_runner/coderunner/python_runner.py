import os

from coderunner.simple_runner import SimpleRunner
from models.language_enum import LanguageEnum
from services.code_executer_service import executor


class PythonRunner(SimpleRunner):
    __file_ext__ = ".py"
    _indentation = 4

    supported_languages = [LanguageEnum.PYTHON]

    def _translate_parameter(self, function_parameter):
        return function_parameter.name

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

    def execute_code(self, return_type, code):
        file_name = self.save_code_to_file(None, self.__file_ext__, code)
        result = self.run_file("python", self.supported_languages[0], file_name, return_type)
        os.remove(file_name)
        return result


executor.register_runner(PythonRunner())