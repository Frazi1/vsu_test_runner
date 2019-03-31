import os
import subprocess
import uuid
from typing import Optional

from app_config import Config
from coderunner.base_code_generator import BaseCodeGenerator
from coderunner.base_runner import BaseRunner


class SimpleRunner(BaseRunner):

    def __init__(self, config: Config, code_generator: BaseCodeGenerator):

        super(SimpleRunner, self).__init__(code_generator)
        self.config = config

    def _run_process(self, command: str, input_data: Optional[str] = None) -> (str, str):
        if input_data:
            command = [command, input_data]
        p = subprocess.run(command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           # input=input_data,
                           encoding="utf-8")
        out = p.stdout
        out = out[:-1]  # remove last line break, because it contains no information
        return out, p.stderr

    def _run_file(self, utility_name: str, file_path: str, input: str) -> (str, str):
        return self._run_process('{} {} 1'.format(utility_name, file_path), input)

    def save_code_to_file(self, name, extension, code):
        if name is None:
            name = uuid.uuid4().hex
        file_path = os.path.join(self.config.tmp_folder_path, name + extension)
        with open(file_path, "w") as file_:
            if isinstance(code, list):
                file_.writelines(code)
            else:
                file_.write(code)
            return file_path
