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

    def _compile_file(self, file_path: str) -> str:
        p = subprocess.Popen('{} {} 1'.format(self.config.csharp_compiler_path,
                                              file_path), stdout=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode("utf-8")
        out = out[:-len(os.linesep)]  # remove last line break, because it contains no information

        return out

    def execute_plain_code(self, return_type: ArgumentType, code: str) -> List[CodeRunResult]:
        file_name = uuid.uuid4().hex
        cs_file_path = self.save_code_to_file(file_name, self.__cs_file_ext__, code)
        exe_file_path = file_name + self.__exe_file_ext__
        try:
            self._compile_file(cs_file_path)
            out = self._run_file("", exe_file_path)
            return []
        except Exception as e:
            os.remove(cs_file_path)
            os.remove(exe_file_path)
            raise
