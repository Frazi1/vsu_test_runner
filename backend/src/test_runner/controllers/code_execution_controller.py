from typing import List

from coderunner.scaffolding_type import ScaffoldingType
from controllers.base_controller import BaseController
from dtos.dtos import CodeExecutionRequestDto, CodeExecutionResponseDto, FunctionScaffoldingDto
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from plugins import QueryParam
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

    @BaseController.get('/code/scaffold/<function_id:int>',
                        returns=FunctionScaffoldingDto,
                        query=[QueryParam("language", LanguageEnum),
                               QueryParam("scaffoldingType", ScaffoldingType, "scaffolding_type")])
    def scaffold_function(self, function_id, language: LanguageEnum, scaffolding_type: ScaffoldingType):
        scaffold_function = self._code_execution_service.scaffold_function(function_id, language, scaffolding_type)
        return scaffold_function

    @BaseController.get('/code/types')
    def supported_code_types(self):
        return [e.name for e in ArgumentType]

    @BaseController.get('/code/languages')
    def supported_languages(self):
        return [e.name for e in self._code_execution_service.get_supported_languages()]

    @BaseController.post('/code/run', accepts=CodeExecutionRequestDto,
                         returns=CodeExecutionResponseDto)
    def execute_code_snippet(self, parsed_body: CodeExecutionRequestDto) -> List[CodeExecutionResponseDto]:
        results = self._code_execution_service.execute_code(parsed_body, None)
        return [CodeExecutionResponseDto(x.file_run_result.input, x.file_run_result.output, parsed_body.client_id) for x
                in results]

    @BaseController.post("/code/run_tests", accepts=CodeExecutionRequestDto, returns=[CodeExecutionResponseDto])
    def run_tests(self, parsed_body: CodeExecutionRequestDto) -> List[CodeExecutionResponseDto]:
        results = self._code_execution_service.execute_tests(parsed_body)
        return results
