from abc import abstractmethod

from coderunner.scaffolding_type import ScaffoldingType
from models.code_snippet import CodeSnippet
from models.function import Function


class BaseCodeGenerator(object):
    @abstractmethod
    def scaffold_function_declaration_text(self, function_: Function, scaffolding_type: ScaffoldingType) -> str:
        pass

    def _translate_parameter(self, function_parameter):
        raise NotImplemented

    @abstractmethod
    def translate_code(self, function_signature: Function, code_snippet: CodeSnippet) -> str:
        pass
