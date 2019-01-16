from sqlalchemy.orm import joinedload

from src.models.TestTemplate import TestTemplate


class TemplatesService:

    def __init__(self):
        pass

    def add_test_template(self, session, test):
        session.add(test)
        session.commit()
        return test.id

    def get_test_templates(self, session):
        return session.query(TestTemplate) \
            .options(joinedload(TestTemplate.questions)) \
            .all()

    def get_test_template_by_id(self, session, id_):
        return session.query(TestTemplate) \
            .options(joinedload(TestTemplate.questions)) \
            .filter(TestTemplate.id == id_) \
            .first()

    def update_test_template(self, session, id_, test):
        db_test = self.get_test_template_by_id(session, id_)
        session.merge(test)
        return db_test


TemplatesServiceInstance = TemplatesService()
