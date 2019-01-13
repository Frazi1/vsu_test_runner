import unittest

from src.dtos.schemas import TestTemplateSchema
from src.models.TestTemplate import TestTemplate


class SerializationTest(unittest.TestCase):
    t = TestTemplate(name="valera", time_limit=10)
    s = TestTemplateSchema()

    def test_serialization(self):
        res = self.s.dump(self.t)
        print res

    def test_deserialization(self):
        text = self.s.dumps(self.t)
        res = self.s.loads(text)
        print res