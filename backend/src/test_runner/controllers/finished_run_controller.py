from controllers.base_controller import BaseController
from dtos.dtos import TestRunDto
from interfaces.service_resolver import ServiceResolver


class FinishedRunController(BaseController):
    def __init__(self,
                 bottle_app,
                 service_resolver  # type: ServiceResolver
                 ):
        super(FinishedRunController, self).__init__(bottle_app, service_resolver.logger, route_prefix='/finished_run')
        self._run_service = service_resolver.run_service

    @BaseController.get('', returns=[TestRunDto])
    def get_finished_runs(self):
        entities = self._run_service.get_finished_test_runs()
        return TestRunDto.from_entity_list(entities)
