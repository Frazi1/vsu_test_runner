from dtos.function_testing_input_schemas import FunctionTestingInputDtoSchema
from interfaces.service_resolver import ServiceResolver
from utils.bottle_controller_plugin.controller_plugin import BaseController


class FunctionTestingController(BaseController):
    def __init__(self, bottle_app, service_resolver):
        # type: ('Bottle', ServiceResolver) -> None
        super(FunctionTestingController, self).__init__(bottle_app, service_resolver.logger,
                                                        route_prefix='functionTesting')

        self._function_service = service_resolver.function_service

    @BaseController.post('<id:int>', request_body_schema=FunctionTestingInputDtoSchema())
    def add_testing_input(self, id, parsed_body):
        # type: (int, FunctionTestingInputDtoSchema) -> None
        self._function_service.add_testing_input(id, parsed_body)
