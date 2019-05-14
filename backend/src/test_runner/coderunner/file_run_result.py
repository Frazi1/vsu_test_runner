from typing import Optional

from models.code_run_status import CodeRunStatus


class FileRunResult(object):
    def __init__(self, input: Optional[str], output: Optional[str], error: Optional[str],
                 status: CodeRunStatus=CodeRunStatus.Success):
        self.input = input
        self.output = output
        self.error = error
        self.status = status
