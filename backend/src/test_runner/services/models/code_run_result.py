from coderunner.file_run_result import FileRunResult
from coderunner.function_run_plan import FunctionRunPlan


class CodeRunResult(object):
    def __init__(self, file_run_result: FileRunResult, run_plan: FunctionRunPlan):
        self.file_run_result = file_run_result
        self.run_plan = run_plan
