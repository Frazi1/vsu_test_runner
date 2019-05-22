import os
import uuid
import shutil
from contextlib import contextmanager
from typing import List, Optional

from app_config import Config
from coderunner.csharp.compilation_error import CompilationError
from coderunner.csharp.csharp_code_generator import CSharpCodeGenerator
from coderunner.file_creation_result import FileCreationResult
from coderunner.file_run_result import FileRunResult
from coderunner.simple_runner import SimpleRunner
from models.code_run_status import CodeRunStatus
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

        cs_file_creation: Optional[FileCreationResult] = None
        try:
            cs_file_creation = self.save_code_to_file(file_name, self.__cs_file_ext__, code)
            exe_file_path = os.path.join(cs_file_creation.created_folder_abs_path,
                                         cs_file_creation.file_name + self.__exe_file_ext__)
            out, err = self._compile_file(cs_file_creation.created_file_abs_path, exe_file_path)
            if not os.path.isfile(exe_file_path):
                raise CompilationError(out)
            yield exe_file_path
        finally:
            if cs_file_creation.created_folder_abs_path is not None \
                    and os.path.isdir(cs_file_creation.created_folder_abs_path):
                shutil.rmtree(cs_file_creation.created_folder_abs_path)

    def _execute_file(self, exe_file_path, input: Optional[str]) -> FileRunResult:
        out, err = self._run_process(exe_file_path, input)
        return FileRunResult(input, out, err, CodeRunStatus.Success)

    def execute_plain_code(self, code: str, inputs: List[str]) -> List[FileRunResult]:
        try:
            with self._save_and_compile_file(code) as exe_file_path:
                executable_id = self._prepare_for_execution(exe_file_path)
                return [self._execute_file(executable_id, input_) for input_ in inputs]
        except CompilationError as e:
            return [FileRunResult(None, None, e.text, CodeRunStatus.CompileError)]

    def _prepare_for_execution(self, exe_file_path):
        return exe_file_path
