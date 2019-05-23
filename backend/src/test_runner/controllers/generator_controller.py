from typing import List

from dtos.dtos import TestingInputGeneratorDto
from services.generator_service import GeneratorService
from utils.bottle_controller_plugin.controller_plugin import BaseController
import utils.validation_utils as validation


class GeneratorController(BaseController):
    def __init__(self, bottle_app, logger=None, generator_service: GeneratorService = None):
        super().__init__(bottle_app, logger, "/generator")

        validation.is_not_none(generator_service, "generator_service")
        self.generator_service = generator_service

    @BaseController.get("<id:int>", returns=TestingInputGeneratorDto)
    def get_by_id(self, id: int) -> TestingInputGeneratorDto:
        return self.generator_service.get_by_id(id)

    @BaseController.get("", returns=[TestingInputGeneratorDto])
    def get_all(self) -> List[TestingInputGeneratorDto]:
        return self.generator_service.get_all()

    @BaseController.post("", accepts=TestingInputGeneratorDto)
    def add(self, parsed_body: TestingInputGeneratorDto) -> int:
        res = self.generator_service.add(parsed_body)
        return res.id
