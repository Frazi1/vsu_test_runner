from bottle import Bottle

from dtos.dtos import TestRunDto
from interfaces.service_resolver import ServiceResolver
from utils.bottle_controller_plugin.controller_plugin import BaseController


class FinishedRunController(BaseController):
    def __init__(self,
                 bottle_app: "Bottle",
                 service_resolver: ServiceResolver
                 ):
        super(FinishedRunController, self).__init__(bottle_app, service_resolver.logger, route_prefix='/finished_run')
        self._run_service = service_resolver.run_service

    @BaseController.get('', returns=[TestRunDto])
    def get_finished_runs(self):
        entities = self._run_service.get_finished_test_runs()
        return TestRunDto.from_entity_list(entities)

    @BaseController.get('<id:int>', returns=TestRunDto)
    def get_finished_run_by_id(self, id: int) -> TestRunDto:
        test_run = self._run_service.get_finished_run_by_id(id)
        dto = TestRunDto.from_entity(test_run)
        return dto

