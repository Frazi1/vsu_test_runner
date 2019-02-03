from sqlalchemy.orm import joinedload

from models.helpers.helper import clone_code_snippet
from models.question_instance import QuestionInstance
from models.test_instance import TestInstance


class InstanceService(object):
    def __init__(self, template_service):
        self.template_service = template_service

    def create_test_instance(self, test_template_id, session):
        test_template = self.template_service.get_test_template_by_id(session, test_template_id)
        question_instances = [QuestionInstance(name=x.name,
                                               time_limit=x.time_limit,
                                               parent_id=x.id,
                                               parent_version=x.version,
                                               solution_code_snippet=clone_code_snippet(x.solution_code_snippet))
                              for x in test_template.questions]
        test_instance = TestInstance(name=test_template.name,
                                     time_limit=test_template.time_limit,
                                     questions=question_instances)
        session.add(test_instance)
        session.commit()
        return test_instance.id

    def get_test_instance(self, test_instance_id, db):
        return db.query(TestInstance) \
            .options(joinedload(TestInstance.questions)) \
            .filter(TestInstance.id == test_instance_id) \
            .first()

    def get_instances(self, db):
        return db.query(TestInstance) \
            .options(joinedload(TestInstance.questions)) \
            .all()

    def update_test_template(self, test_instance, db):
        db_test_instance = self.get_test_instance(test_instance.id, db)
        db.merge(test_instance)
        db.commit()
        return db_test_instance
