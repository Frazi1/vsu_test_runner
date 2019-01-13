import unittest

from src.dtos.schemas import TestTemplateSchema
from src.models.TestQuestionTemplate import TestQuestionTemplate
from src.models.TestTemplate import TestTemplate


class SerializationTest(unittest.TestCase):
    t = TestTemplate(name="valera", time_limit=10, questions=[TestQuestionTemplate(name="q1")])
    s = TestTemplateSchema()

    def test_serialization(self):
        res = self.s.dumps(self.t).data
        print res

    def test_deserialization(self):
        text = self.s.dumps(self.t).data
        res = self.s.loads(text)
        print res.data