import unittest

from dtos.schemas import TestTemplateDtoSchema
from models.test_question_template import TestQuestionTemplate
from models.test_template import TestTemplate


class SerializationTest(unittest.TestCase):
    t = TestTemplate(name="valera", time_limit=10, questions=[TestQuestionTemplate(name="q1")])
    s = TestTemplateDtoSchema()

    def test_serialization(self):
        res = self.s.dumps(self.t).data
        print res

    def test_deserialization(self):
        text = self.s.dumps(self.t).data
        res = self.s.loads(text)
        print res.data