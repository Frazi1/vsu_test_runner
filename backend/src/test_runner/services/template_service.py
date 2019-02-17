from sqlalchemy.orm import joinedload

from models.test_template import TestTemplate
from services.base_service import BaseService


class TemplateService(BaseService):

    def __init__(self):
        pass

    def add_test_template(self, test):
        self._db.add(test)
        self._db.commit()
        return test.id

    def get_test_templates(self, include_deleted=False):
        q = self._db.query(TestTemplate).options(joinedload(TestTemplate.questions))
        if include_deleted is False:
            q = q.filter(TestTemplate.is_deleted == False)
        test_templates = q.all()
        return test_templates

    def get_test_template_by_id(self, id_):
        # type: (int) -> TestTemplate
        return self._db.query(TestTemplate) \
            .options(joinedload(TestTemplate.questions)) \
            .filter(TestTemplate.id == id_) \
            .first()

    def update_test_template(self, id_, test):
        db_test = self.get_test_template_by_id(id_)
        self._db.merge(test)
        return db_test

    def delete_test_template(self, id_):
        test_template = self.get_test_template_by_id(id_)
        test_template.is_deleted = True

        for question in test_template.questions:
            question.is_deleted = True
