from sqlalchemy.orm import joinedload

from src.db_config import Session
from src.models.TestQuestionTemplate import TestQuestionTemplate
from src.models.TestTemplate import TestTemplate


class TemplatesService:

    def __init__(self):
        self._session = Session()

    def add_question(self, name, time_limit=None):
        t = TestTemplate(name)
        t.questions.append(TestQuestionTemplate("Question 1", ))
        self._session.add(t)
        self._session.commit()

    def get_test_templates(self):
        return self._session.query(TestTemplate)\
            .options(joinedload(TestTemplate.questions))\
            .all()

s = TemplatesService()
# s.add_question("Test 1")
print "\n"
print [x.questions for x in s.get_test_templates()]
