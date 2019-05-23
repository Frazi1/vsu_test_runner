from typing import TypeVar, Union

from models.db_testing_input_generator import DbTestingInputGenerator
from models.repositories.base_repository import BaseRepository


class GeneratorRepository(BaseRepository):
    T = DbTestingInputGenerator
