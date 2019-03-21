import subprocess
import uuid
from typing import List

import os

from app_config import Config
from coderunner.csharp.csharp_code_generator import CSharpCodeGenerator

from coderunner.simple_runner import SimpleRunner
from dtos.dtos import CodeRunResult
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum


class CSharpRunner(SimpleRunner):
    __cs_file_ext__ = ".cs"
    __exe_file_ext__ = ".exe"

    def __init__(self, config: Config):
        self.code_generator = CSharpCodeGenerator()
        super().__init__(config, self.code_generator)

    @property
    def supported_language(self):
        return LanguageEnum.CSHARP

    def _compile_file(self, cs_file_path: str, out_exe_file_path) -> str:
        return self._run_process('{csc} -out:{exe_file} {cs_file}'.format(csc=self.config.csharp_compiler_path,
                                                                          exe_file=out_exe_file_path,
                                                                          cs_file=cs_file_path))

    def _execute_file(self, exe_file_path):
        return self._run_process(exe_file_path)

    def execute_plain_code(self, return_type: ArgumentType, code: str) -> List[CodeRunResult]:
        file_name = uuid.uuid4().hex
        cs_file_path = self.save_code_to_file(file_name, self.__cs_file_ext__, code)
        exe_file_path = os.path.splitext(cs_file_path)[0] + self.__exe_file_ext__
        try:
            self._compile_file(cs_file_path, exe_file_path)
            out = self._execute_file(exe_file_path)
            return []
        except Exception as e:
            os.remove(cs_file_path)
            os.remove(exe_file_path)
            raise
