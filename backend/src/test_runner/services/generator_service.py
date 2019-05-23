from typing import List

from dtos.dtos import TestingInputGeneratorDto
from models.db_testing_input_generator import DbTestingInputGenerator
from models.repositories.generator_repository import GeneratorRepository
from services.base_service import BaseService


class GeneratorService(BaseService):
    def __init__(self, generator_repository: GeneratorRepository) -> None:
        super().__init__()
        self.generator_repository = generator_repository

    def get_by_id(self, id_: int) -> TestingInputGeneratorDto:
        db_generator: DbTestingInputGenerator = self.generator_repository.get_by_id(id_)
        return TestingInputGeneratorDto.from_entity(db_generator)

    def get_all(self) -> List[TestingInputGeneratorDto]:
        entities = self.generator_repository.get_all()
        dtos = TestingInputGeneratorDto.from_list(entities)
        return dtos

    def add(self, generator_dto: TestingInputGeneratorDto) -> DbTestingInputGenerator:
        entity = generator_dto.to_entity()
        res = self.generator_repository.add(entity)
        self.generator_repository.commit()
        return res
