from controllers.base_controller import BaseController
from dtos.schemas import TestTemplateSchema
from logger.logger import ILogger
from services.template_service import TemplateService


class TemplateController(BaseController):
    def __init__(self, bottle_app,
                 templates_service, # type: TemplateService
                 logger # type: ILogger
                 ):
        super(TemplateController, self).__init__(bottle_app, logger)
        self.templates_service = templates_service

    @BaseController.get('/template', response_schema=TestTemplateSchema(many=True))
    def get_test_templates(self):
        return self.templates_service.get_test_templates()

    @BaseController.post('/template', request_body_schema=TestTemplateSchema())
    def add_test_template(self, parsed_body):
        id_ = self.templates_service.add_test_template(parsed_body)
        return id_

    @BaseController.get('/template/<id:int>', response_schema=TestTemplateSchema())
    def get_test_template_by_id(self, id):
        res = self.templates_service.get_test_template_by_id(id)
        return res

    @BaseController.put('/template/<id:int>', request_body_schema=TestTemplateSchema(), response_schema=TestTemplateSchema())
    def update_test_template(self, id, parsed_body):
        return self.templates_service.update_test_template(id, parsed_body)

    @BaseController.delete('/template/<id:int>')
    def delete_test_template(self, id):
        self.templates_service.delete_test_template(id)
