from typing import List

from dtos.dtos import TestTemplateDto
from logger.logger import ILogger
from services.template_service import TemplateService
from utils.bottle_controller_plugin.controller_plugin import BaseController
from utils.bottle_query_parser_plugin.query_parser_plugin import QueryParam


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

    @BaseController.put('/template/<id:int>', accepts=TestTemplateDto)
    def update_test_template(self, id, parsed_body):
        # type: (int, TestTemplateDto) -> int
        template = parsed_body.to_entity()
        self.templates_service.update_test_template_and_calc_expected_results(template)
        return id

    @BaseController.delete('/template/<id:int>')
    def delete_test_template(self, id):
        self.templates_service.delete_test_template(id)

    @BaseController.put('/template/restore/<id:int>')
    def restore_test_template(self, id):
        self.templates_service.restore(id)
        return id
