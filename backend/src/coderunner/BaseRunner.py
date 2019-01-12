from abc import abstractproperty, abstractmethod

from src.services.CodeExecuterService import Registrator


class BaseRunner(object):
    # __metaclass__ = Registrator

    def __init__(self):
        pass

    @abstractproperty
    def supported_languages(self):
        pass

    def _translate_parameter(self, function_parameter):
        raise NotImplemented

    @abstractmethod
    def translate_code(self, function_signature, code_snippet):
        pass

    def execute_snippet(self, function_signature, code_snippet):
        code = self.translate_code(function_signature, code_snippet)
        return self.execute_code(function_signature.return_type, code)

    @abstractmethod
    def execute_code(self, return_type, code):
        pass
