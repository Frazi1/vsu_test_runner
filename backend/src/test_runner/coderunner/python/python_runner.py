import os
import re
from typing import List

from app_config import Config
from coderunner.function_run_plan import FunctionRunPlan
from coderunner.python.python_code_generator import PythonCodeGenerator
from coderunner.simple_runner import SimpleRunner
from dtos.dtos import CodeRunResult
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from shared.value_converter import ValueConverter


class PythonRunner(SimpleRunner):
    __file_ext__ = ".py"

    @property
    def supported_language(self):
        return LanguageEnum.PYTHON

    code_generator = PythonCodeGenerator()

    def __init__(self, config):
        # type: (Config) -> None
        super(PythonRunner, self).__init__(config)

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

        ready_template = self.code_generator.prepare_code_from_template(template_text,
                                                                        function_run_plans,
                                                                        function_declaration_code)
        return self.execute_plain_code(function_run_plans[0].function.return_type, ready_template)
