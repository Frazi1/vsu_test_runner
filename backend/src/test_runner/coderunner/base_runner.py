from abc import abstractproperty, abstractmethod

from dtos.dtos import CodeRunResult
from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function import Function
from models.language_enum import LanguageEnum


class BaseRunner(object):
    def __init__(self):
        pass

    @abstractproperty
    def supported_languages(self):
        pass

    def _translate_parameter(self, function_parameter):
        raise NotImplemented

    @abstractmethod
    def translate_code(self, function_signature, code_snippet):
        # type: (Function, CodeSnippet) -> str
        pass

    def execute_snippet(self, function_signature, code_snippet):
        # type: (Function, CodeSnippet) -> CodeRunResult

        code = self.translate_code(function_signature, code_snippet)
        return self.execute_plain_code(function_signature.return_type, code)

    @abstractmethod
    def execute_plain_code(self, return_type, code):
        # type: (ArgumentType, str) -> CodeRunResult
        pass

    @abstractmethod
    def scaffold_function_declaration_text(self, function_):
        # type: (Function, LanguageEnum) -> str
        pass
