import enum


class CodeRunStatus(enum.Enum):
    Success = 0
    CompileError = 1
    RuntimeError = 2
