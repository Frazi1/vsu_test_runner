import os
import uuid
from contextlib import contextmanager
from typing import List, Optional

from app_config import Config
from coderunner.csharp.compilation_error import CompilationError
from coderunner.csharp.csharp_code_generator import CSharpCodeGenerator
from coderunner.file_run_result import FileRunResult
from coderunner.simple_runner import SimpleRunner
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
        return self._run_process('"{csc}" -out:{exe_file} {cs_file}'.format(csc=self.config.csharp_compiler_path,
                                                                            exe_file=out_exe_file_path,
                                                                            cs_file=cs_file_path))

    @contextmanager
    def _save_and_compile_file(self, code: str, file_name: str = None):
        if not file_name:
            file_name = uuid.uuid4().hex

        cs_file_path = None
        exe_file_path = None
        try:
            cs_file_path = self.save_code_to_file(file_name, self.__cs_file_ext__, code)
            exe_file_path = os.path.splitext(cs_file_path)[0] + self.__exe_file_ext__
            out, err = self._compile_file(cs_file_path, exe_file_path)
            if not os.path.isfile(exe_file_path): raise CompilationError(out)
            yield exe_file_path
        finally:
            if cs_file_path is not None and os.path.isfile(cs_file_path):
                os.remove(cs_file_path)
            if exe_file_path is not None and os.path.isfile(exe_file_path):
                os.remove(exe_file_path)

    def _execute_file(self, exe_file_path, input: Optional[str]) -> FileRunResult:
        out, err = self._run_process(exe_file_path, input)
        return FileRunResult(input, out, err)

    def execute_plain_code(self, code: str, inputs: List[str]) -> List[FileRunResult]:
        with self._save_and_compile_file(code) as exe_file_path:
            return [self._execute_file(exe_file_path, input_) for input_ in inputs]
