from sqlalchemy.orm import joinedload

from src.models.TestQuestionTemplate import TestQuestionTemplate
from src.models.TestTemplate import TestTemplate


class TemplatesService:

    def __init__(self):
        pass

    def add_test_template(self, session, test):
        session.add(test)
        session.commit()

    def add_question(self, session, name, time_limit=None):
        t = TestTemplate(name)
        t.questions.append(TestQuestionTemplate("Question 1", ))
        session.add(t)

    def get_test_templates(self, session):
        return session.query(TestTemplate) \
            .options(joinedload(TestTemplate.questions)) \
            .all()


TemplatesServiceInstance = TemplatesService()