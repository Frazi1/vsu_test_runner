from controllers.base_controller import BaseController


class InstanceController(BaseController):
    def __init__(self, bottle_app, instance_service, logger):
        super(InstanceController, self).__init__(bottle_app, logger)
        self.instance_service = instance_service

    @BaseController.post('/instance/<id:int>')
    def create_instance(self, db, id):
        return self.instance_service.create_test_instance(id, db)
