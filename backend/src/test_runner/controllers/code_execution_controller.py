from bottle import request

from controllers.base_controller import BaseController
from dtos.schemas import FunctionScaffoldingDtoSchema
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from services.code_executer_service import CodeExecuterService


class CodeExecutionController(BaseController):
    def __init__(self, bottle_app, logger,
                 code_execution_service  # type: CodeExecuterService
                 ):
        super(CodeExecutionController, self).__init__(bottle_app, logger)
        self._code_execution_service = code_execution_service

    @BaseController.get('/code/scaffold/<function_id:int>', response_schema=FunctionScaffoldingDtoSchema())
    def scaffold_function(self, function_id):
        language = request.query['language']
        scaffold_function = self._code_execution_service.scaffold_function(function_id, LanguageEnum[language])
        return scaffold_function

    @BaseController.get('/code/types')
    def supported_code_types(self):
        return ArgumentType.__members__.keys()

    @BaseController.get('/code/languages')
    def supported_languages(self):
        return [e.name for e in self._code_execution_service.get_supported_languages()]
