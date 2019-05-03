from utils.business_error import BusinessException


class CompilationError(BusinessException):
    def __init__(self, text):
        self.text = text
