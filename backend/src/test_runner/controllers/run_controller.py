from controllers.base_controller import BaseController
from dtos.dtos import TestRunDto
from dtos.run_schema import TestRunSchema
from services.run_service import RunService


class RunController(BaseController):

    def __init__(self,
                 bottle_app,
                 run_service, # type: RunService
                 logger):
        super(RunController, self).__init__(bottle_app, logger)
        self._run_service = run_service

    @BaseController.get('/run/<test_run_id:int>', response_schema=TestRunSchema())
    def get_test_run_by_id(self, test_run_id, db):
        run = self._run_service.get_active_test_run(test_run_id, db)
        return TestRunDto.map_from(run)

    @BaseController.post('/run/<test_instance_id:int>')
    def start_test_run(self, test_instance_id, db):
        return self._run_service.start_run_from_instance(test_instance_id, db)
