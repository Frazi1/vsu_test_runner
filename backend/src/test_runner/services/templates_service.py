from sqlalchemy.orm import joinedload

from models.test_template import TestTemplate


class TemplatesService:

    def __init__(self):
        pass

    def add_test_template(self, session, test):
        try:
            session.add(test)
            session.commit()
            return test.id
        except Exception, e:
            a= e


    def get_test_templates(self, session):
        # for x in range(1, 100000):
        #     session.add(TestTemplate(name="Template:{}".format(x)))
        # session.commit()
        print "Enter"
        questions__all = session.query(TestTemplate).options(joinedload(TestTemplate.questions)).all()
        print "Exit"
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



TemplatesServiceInstance = TemplatesService()
