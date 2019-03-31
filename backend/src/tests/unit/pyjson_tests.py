import unittest

from dtos.dtos import CodeExecutionRequestDto
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from utils.pyjson.pyjson import PyJsonConverter


class PyJsonTest(unittest.TestCase):
    serializer = PyJsonConverter()

    def test_dto(self):
        dto = CodeExecutionRequestDto("def test():pass", LanguageEnum.PYTHON, True, 10, ArgumentType.ARRAY_INTEGER,
                                      None)
        json_text = self.serializer.to_json(dto)
        cls = self.serializer.from_json(json_text, CodeExecutionRequestDto)
