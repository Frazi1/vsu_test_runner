from coderunner.base_runner import BaseRunner
from dtos.dtos import FunctionScaffoldingDto
from models.language_enum import LanguageEnum
from services.function_service import FunctionService


class CodeExecuterService:
    def __init__(self,
                 function_service  # type: FunctionService
                 ):
        self._function_service = function_service

    _runners = {}

    def register_runner(self, cls_):
        print "TYPE: {}".format(type(cls_))
        try:
            languages = cls_.supported_languages
            for lang in languages:
                if lang not in self._runners:
                    print "REGISTER:{}, language:{}".format(cls_, lang)
                    self._runners[lang] = cls_
        except Exception, e:
            print e.message

    def _find_runner(self, language):
        # type: (LanguageEnum) -> BaseRunner
        return self._runners[language]

    def get_supported_languages(self):
        return self._runners.keys()

    def execute_snippet(self, function_signature, code_snippet):
        runner = self._find_runner(code_snippet.language)
        return runner.execute_snippet(function_signature, code_snippet)

    def execute_code(self, language, return_type, code):
        runner = self._find_runner(language)
        return runner.execute_code(return_type, code)

    def scaffold_function(self, function_id, language):
        # type: (int, LanguageEnum) -> FunctionScaffoldingDto
        func = self._function_service.get_function_by_id(function_id)
        runner = self._find_runner(language)
        code = runner.scaffold_function_declaration_text(func)
        return FunctionScaffoldingDto(code, language, func)
