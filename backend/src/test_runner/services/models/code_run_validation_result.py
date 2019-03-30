from services.models.code_run_result import CodeRunResult


class CodeRunValidationResult(object):
    def __init__(self, code_run_result: CodeRunResult, is_valid: bool):
        self.code_run_result = code_run_result
        self.is_valid = is_valid
