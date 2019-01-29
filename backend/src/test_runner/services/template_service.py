from sqlalchemy.orm import joinedload

from models.test_template import TestTemplate


class TemplateService:

    def __init__(self):
        pass

    def add_test_template(self, session, test):
        try:
            session.add(test)
            session.commit()
            return test.id
        except Exception, e:
            a= e


    def get_test_templates(self, session, include_deleted=False):

        q = session.query(TestTemplate).options(joinedload(TestTemplate.questions))
        if include_deleted is False:
            q = q.filter(TestTemplate.is_deleted == False)
        questions__all = q.all()
        return questions__all

    def get_test_template_by_id(self, session, id_):
        return session.query(TestTemplate) \
            .options(joinedload(TestTemplate.questions)) \
            .filter(TestTemplate.id == id_) \
            .first()

    def update_test_template(self, session, id_, test):
        db_test = self.get_test_template_by_id(session, id_)
        session.merge(test)
        return db_test

    def delete_test_template(self, session, id_):
        test_template = self.get_test_template_by_id(session, id_)
        test_template.is_deleted = True

        for question in test_template.questions:
            question.is_deleted = True
