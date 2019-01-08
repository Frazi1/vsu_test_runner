import subprocess
from BaseRunner import BaseRunner


class PythonRunner(BaseRunner):
    __file_ext__ = ".py"
    _indentation = 4

    def _translate_parameter(self, function_parameter):
        return function_parameter.name

    def _indent_line(self, line, last):
        res = " " * self._indentation + line
        if last is not True:
            res += "\n"
        return res

    def _translate_code(self, function_signature, code_snippet):
        parameters = [self._translate_parameter(x) for x in function_signature.parameters]
        signature = "def {name}({parameters}):\n".format(name=function_signature.name,
                                                         parameters=", ".join(parameters))

        code_lines = code_snippet.code.splitlines()
        formatted_code = "".join(
            [(self._indent_line(x, index == len(code_lines) - 1)) for index, x in enumerate(code_lines)])
        return signature + formatted_code

    def execute(self, function_signature, code_snippet):
        code = self._translate_code(function_signature, code_snippet)
        file_name = self.write_code(code)

    def _run_file(self, file_path, return_type):
        p = subprocess.Popen('python {} 1'.format(file_path), stdout=subprocess.PIPE)
        out, err = p.communicate()
        print out
        print err

