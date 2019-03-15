import os
import subprocess
import uuid
from typing import List

from app_config import Config
from coderunner.base_runner import BaseRunner
from dtos.dtos import CodeRunResult
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from shared.value_converter import ValueConverter


class SimpleRunner(BaseRunner):

    def __init__(self, config):
        # type: (Config)-> None

        super(SimpleRunner, self).__init__()
        self._config = config

    def run_file(self, utility_name: str, language: LanguageEnum, file_path: str, return_type: ArgumentType
                 ) -> List[CodeRunResult]:
        p = subprocess.Popen('{} {} 1'.format(utility_name,
                                              file_path), stdout=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode("utf-8")
        out = out[:-len(os.linesep)]  # remove last line break, because it contains no information

        if err is not None:
            return [CodeRunResult(language, None, return_type, err)]

        raw_results = out.split(os.linesep)
        typed_results = [CodeRunResult(language, ValueConverter.from_string(return_type, res, parse_str=False),
                                       return_type) for res in raw_results]
        return typed_results

    def save_code_to_file(self, name, extension, code):
        if name is None:
            name = uuid.uuid4().hex
        file_path = os.path.join(self._config.tmp_folder_path, name + extension)
        with open(file_path, "w") as file_:
            if isinstance(code, list):
                file_.writelines(code)
            else:
                file_.write(code)
            return file_path
