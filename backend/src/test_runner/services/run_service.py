from models.test_run import TestRun
from services.base_service import BaseService


class RunService(BaseService):

    def __init__(self, instance_service):
        super(RunService, self).__init__()
        self.instance_service = instance_service

    def start_run_from_instance(self, instance_id, db):
        test_instance = self.instance_service.get_test_instance(instance_id, db)
        test_run = TestRun(test_instance=test_instance)
        db.add(test_run)
        db.commit()
        return test_run.id
