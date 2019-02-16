from controllers.base_controller import BaseController
from dtos.dtos import TestInstanceUpdate
from dtos.instance_schema import TestInstanceSchema, TestInstanceUpdateSchema
from logger.logger import ILogger
from models.test_instance import TestInstance
from services.instance_service import InstanceService


class InstanceController(BaseController):
    def __init__(self,
                 bottle_app,
                 instance_service,  # type: InstanceService
                 logger  # type: ILogger
                 ):
        super(InstanceController, self).__init__(bottle_app, logger)
        self.instance_service = instance_service

    @BaseController.get('/instance', response_schema=TestInstanceSchema(many=True))
    def get_instances(self):
        instances = self.instance_service.get_instances()
        return instances

    @BaseController.get('/instance/<instance_id:int>', response_schema=TestInstanceSchema())
    def get_test_instance_by_id(self, instance_id):
        res = self.instance_service.get_test_instance(instance_id)
        return res

    @BaseController.put('/instance/<instance_id:int>',
                        request_body_schema=TestInstanceUpdateSchema(),
                        response_schema=TestInstanceSchema())
    def update_test_instance_by_id(self, parsed_body, instance_id):
        # type: (TestInstanceUpdate, int) -> TestInstance

        res = self.instance_service.update_test_instance(instance_id, parsed_body)
        return res

    @BaseController.post('/instance/create/<template_id:int>', )
    def create_instance(self, db, template_id):
        return self.instance_service.create_test_instance(template_id, db)
