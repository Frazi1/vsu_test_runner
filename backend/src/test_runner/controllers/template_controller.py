from controllers.base_controller import BaseController
from dtos.schemas import TestTemplateSchema


class TemplateController(BaseController):
    def __init__(self, bottle_app, templates_service, logger):
        super(TemplateController, self).__init__(bottle_app, logger)
        self.templates_service = templates_service

    @BaseController.get('/template', response_schema=TestTemplateSchema(many=True))
    def get_test_templates(self, db):
        return self.templates_service.get_test_templates(db)

    @BaseController.post('/template', request_body_schema=TestTemplateSchema())
    def add_test_template(self, db, parsed_body):
        id_ = self.templates_service.add_test_template(db, parsed_body)
        return id_

    @BaseController.get('/template/<id:int>', response_schema=TestTemplateSchema())
    def get_test_template_by_id(self, db, id):
        res = self.templates_service.get_test_template_by_id(db, id)
        return res

    @BaseController.put('/template/<id:int>', request_body_schema=TestTemplateSchema(), response_schema=TestTemplateSchema())
    def update_test_template(self, db, id, parsed_body):
        return self.templates_service.update_test_template(db, id, parsed_body)
