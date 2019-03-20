import os
import subprocess
import uuid

from app_config import Config
from coderunner.base_code_generator import BaseCodeGenerator
from coderunner.base_runner import BaseRunner


class SimpleRunner(BaseRunner):

    def __init__(self, config: Config, code_generator: BaseCodeGenerator):

        super(SimpleRunner, self).__init__(code_generator)
        self._config = config

    def run_file(self, utility_name: str, file_path: str) -> str:
        p = subprocess.Popen('{} {} 1'.format(utility_name,
                                              file_path), stdout=subprocess.PIPE)
        out, err = p.communicate()
        out = out.decode("utf-8")
        out = out[:-len(os.linesep)]  # remove last line break, because it contains no information

        return out

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
