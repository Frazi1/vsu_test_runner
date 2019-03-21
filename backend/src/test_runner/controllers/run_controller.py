from typing import List

from controllers.base_controller import BaseController
from dtos.dtos import TestRunDto, TestRunAnswerUpdateDto
from dtos.run_schema import TestRunSchema
from services.run_service import RunService


class RunController(BaseController):

    def __init__(self,
                 bottle_app,
                 run_service,  # type: RunService
                 logger):
        super(RunController, self).__init__(bottle_app, logger, route_prefix="/run")
        self._run_service = run_service

    @BaseController.get('<test_run_id:int>', returns=TestRunDto)
    def get_test_run_by_id(self, test_run_id):
        run = self._run_service.get_active_test_run(test_run_id)
        return TestRunDto.from_entity(run)

    @BaseController.get('', response_schema=TestRunSchema(many=True))
    def get_test_runs(self):
        runs = self._run_service.get_all_active_test_runs()
        dtos = [TestRunDto.from_entity(x) for x in runs]
        return sorted(dtos, key=lambda x: x.id)

    @BaseController.post('<test_instance_id:int>')
    def start_test_run(self, test_instance_id):
        return self._run_service.start_run_from_instance(test_instance_id)

    @BaseController.put('<test_run_id:int>', accepts=[TestRunAnswerUpdateDto])
    def update_run_answers(self, test_run_id, parsed_body):
        # type: (int, List[TestRunAnswerUpdateDto]) -> int
        self._run_service.update_test_run_answers(test_run_id, parsed_body)
        return test_run_id

    @BaseController.put('finish/<test_run_id:int>', accepts=[TestRunAnswerUpdateDto])
    def finish_test_run(self, test_run_id, parsed_body):
        # type: (int, List[TestRunAnswerUpdateDto]) -> int
        self._run_service.finish_test_run(test_run_id, parsed_body)
        return test_run_id