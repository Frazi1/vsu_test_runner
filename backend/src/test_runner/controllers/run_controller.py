from controllers.base_controller import BaseController


class RunController(BaseController):

    def __init__(self, bottle_app, run_service, logger):
        super(RunController, self).__init__(bottle_app, logger)
        self.run_service = run_service

    @BaseController.post('/run/<test_instance_id>')
    def start_test_run(self, test_instance_id, db):
        return self.run_service.start_run_from_instance(test_instance_id, db)
