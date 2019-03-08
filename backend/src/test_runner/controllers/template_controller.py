from typing import List

from controllers.base_controller import BaseController
from dtos.dtos import TestTemplateDto
from logger.logger import ILogger
from plugins import QueryParam
from services.template_service import TemplateService


class TemplateController(BaseController):
    def __init__(self, bottle_app,
                 templates_service,  # type: TemplateService
                 logger  # type: ILogger
                 ):
        super(TemplateController, self).__init__(bottle_app, logger)
        self.templates_service = templates_service

    @BaseController.get('/template', returns=[TestTemplateDto],
                        query=[QueryParam('includeDeleted', bool, 'include_deleted')])
    def get_test_templates(self, include_deleted):
        # type: (bool) -> List[TestTemplateDto]

        templates = self.templates_service.get_test_templates(include_deleted)
        templates_dtos = TestTemplateDto.list_of(templates)
        return templates_dtos

    @BaseController.post('/template', accepts=TestTemplateDto)
    def add_test_template(self, parsed_body):
        # type: (TestTemplateDto) -> int

        test_template = parsed_body.to_entity()
        id_ = self.templates_service.add_test_template(test_template)
        return id_

    @BaseController.get('/template/<id:int>', returns=TestTemplateDto)
    def get_test_template_by_id(self, id):
        template = self.templates_service.get_test_template_by_id(id)
        dto = TestTemplateDto.from_entity(template)
        return dto

    @BaseController.put('/template/<id:int>', accepts=TestTemplateDto,
                        returns=TestTemplateDto)
    def update_test_template(self, id, parsed_body):
        # type: (int, TestTemplateDto) -> TestTemplateDto
        template = parsed_body.to_entity()
        updated_template = self.templates_service.update_test_template(id, template)
        return TestTemplateDto.from_entity(updated_template)

    @BaseController.delete('/template/<id:int>')
    def delete_test_template(self, id):
        self.templates_service.delete_test_template(id)

    @BaseController.put('/template/restore/<id:int>')
    def restore_test_template(self, id):
        self.templates_service.restore(id)
        return id
