import os
import re
from typing import List

from app_config import Config
from coderunner.file_run_result import FileRunResult
from coderunner.function_run_plan import FunctionRunPlan
from coderunner.python.python_code_generator import PythonCodeGenerator
from coderunner.simple_runner import SimpleRunner
from dtos.dtos import CodeRunResultDto
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from shared.value_converter import ValueConverter


class PythonRunner(SimpleRunner):
    __file_ext__ = ".py"

    @property
    def supported_language(self):
        return LanguageEnum.PYTHON

    def __init__(self, config: Config):
        self.code_generator = PythonCodeGenerator()
        super(PythonRunner, self).__init__(config, self.code_generator)

    def _parse_out_file(self, out: str, language: LanguageEnum, return_type: ArgumentType) -> List[CodeRunResultDto]:
        regex = re.compile(
            r'<StartIteration>{line_splitter}(.*?){line_splitter}<EndIteration>'.format(line_splitter=os.linesep),
            re.RegexFlag.MULTILINE | re.RegexFlag.DOTALL)
        raw_results = regex.findall(out)
        typed_results = [CodeRunResultDto(language,
                                          ValueConverter.to_string(return_type,
                                                                   ValueConverter.from_string(return_type, res,
                                                                                              parse_str=False)),
                                          return_type) for res in raw_results]
        return typed_results

    def execute_plain_code(self, code: str, inputs: List[str]) -> List[FileRunResult]:
        file_path = self.save_code_to_file(None, self.__file_ext__, code)
        try:
            results = []
            for input_ in inputs:
                out, err = self._run_file("python", file_path, input_)
                results.append(FileRunResult(input_, out, err))
            return results
        finally:
            os.remove(file_path)

    def execute_default_template(self,
                                 function_declaration_code: str,
                                 function_run_plans: List[FunctionRunPlan]) -> List[CodeRunResultDto]:
        with open(self.config.python_default_template_path, "r") as file_:
            template_text = file_.read()

        ready_template = self.code_generator.prepare_code_from_template(template_text,
                                                                        function_run_plans,
                                                                        function_declaration_code)
        return self.execute_plain_code(function_run_plans[0].function.return_type, ready_template)
