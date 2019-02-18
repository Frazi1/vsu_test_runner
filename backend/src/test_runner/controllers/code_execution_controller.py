from bottle import request

from controllers.base_controller import BaseController
from dtos.dtos import CodeExecutionRequestDto, CodeExecutionResponseDto
from dtos.schemas import FunctionScaffoldingDtoSchema, CodeExecutionRequestSchema, CodeExecutionResponseSchema
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from services.code_executer_service import CodeExecuterService
from services.function_service import FunctionService


class CodeExecutionController(BaseController):
    def __init__(self, bottle_app, logger,
                 code_execution_service,  # type: CodeExecuterService
                 function_service,  # type: FunctionService
                 ):
        super(CodeExecutionController, self).__init__(bottle_app, logger)
        self._function_service = function_service
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

    @BaseController.post('/code/run', request_body_schema=CodeExecutionRequestSchema(),
                         response_schema=CodeExecutionResponseSchema())
    def execute_code_snippet(self, parsed_body):
        # type: (CodeExecutionRequestDto)-> CodeExecutionResponseDto

        code_run_result = self._code_execution_service.execute_code(parsed_body)
        return CodeExecutionResponseDto(code_run_result, parsed_body.client_id)
