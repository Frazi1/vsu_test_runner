from controllers.base_controller import BaseController
from dtos.instance_schema import TestInstanceSchema


class InstanceController(BaseController):
    def __init__(self, bottle_app, instance_service, logger):
        super(InstanceController, self).__init__(bottle_app, logger)
        self.instance_service = instance_service

    @BaseController.get('/instance', response_schema=TestInstanceSchema(many=True))
    def get_instances(self, db):
        instances = self.instance_service.get_instances(db)
        return instances

    @BaseController.get('/instance/<instance_id:int>', response_schema=TestInstanceSchema())
    def get_test_instance_by_id(self, instance_id, db):
        res = self.instance_service.get_test_instance(instance_id, db)
        return res

    @BaseController.post('/instance/create/<template_id:int>', )
    def create_instance(self, db, template_id):
        return self.instance_service.create_test_instance(template_id, db)
