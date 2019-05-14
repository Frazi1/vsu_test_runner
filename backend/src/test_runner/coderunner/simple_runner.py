import os
import subprocess
import uuid
import re
from itertools import takewhile
from typing import Optional

from app_config import Config
from coderunner.base_code_generator import BaseCodeGenerator
from coderunner.base_runner import BaseRunner


class SimpleRunner(BaseRunner):

    def __init__(self, config: Config, code_generator: BaseCodeGenerator):

        super(SimpleRunner, self).__init__(code_generator)
        self.config = config

    def _run_process(self, command: str, input_data: Optional[str] = None) -> (str, str):
        # if input_data is not None:
            # command = [command, input_data]
        p = subprocess.run(command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           input=input_data.encode("utf-8") if input_data is not None else b'',
                           # universal_newlines=True,
                           # encoding="utf-8"
                           )

        out = self._decode_text(p.stdout)
        if re.search(".*\r\n$", out):
            out = out.rstrip("\r\n")  # remove last line break, because it contains no information

        err = self._decode_text(p.stderr)
        err = err[:-1] if err is not None else None
        return out, err

    def _decode_text(self, bytes) -> str:
        return self._decode(bytes, "utf-8") or self._decode(bytes, "cp866") or self._decode(bytes, "windows-1251")

    def _decode(self, bytes, encoding):
        if isinstance(bytes, str):
            return bytes
        try:
            return bytes.decode(encoding)
        except Exception as e:
            return None

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
