import subprocess
import uuid

from coderunner.base_runner import BaseRunner
from dtos.dtos import CodeRunResult
from models.argument_type import ArgumentType
from shared.value_converter import ValueConverter


class SimpleRunner(BaseRunner):
    def run_file(self, utility_name, language, file_path, return_type):
        p = subprocess.Popen('{} {} 1'.format(utility_name,
                                              file_path), stdout=subprocess.PIPE)
        out, err = p.communicate()

        if err is not None:
            return CodeRunResult(language, None, return_type, err)

        # 'print' in python adds '\n' after its output. So remove it.
        if len(out) > 0 and return_type is ArgumentType.STRING and out[-1] == "\n":
            out = out[:-1]
        typed_result = ValueConverter.from_string(return_type, out)
        return CodeRunResult(language, typed_result, return_type)

    def save_code_to_file(self, name, extension, code):
        if name is None:
            name = uuid.uuid4().get_hex()
        with open(name + extension, "w") as file_:
            if isinstance(code, list):
                file_.writelines(code)
            else:
                file_.write(code)
            return file_.name
