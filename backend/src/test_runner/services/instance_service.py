from sqlalchemy.orm import joinedload

from dtos.dtos import TestInstanceUpdate
from models.helpers.helper import clone_code_snippet
from models.question_instance import QuestionInstance
from models.test_instance import TestInstance
from services.base_service import BaseService
from services.template_service import TemplateService


class InstanceService(BaseService):
    def __init__(self,
                 template_service  # type: TemplateService
                 ):
        self._template_service = template_service

    def create_test_instance(self, test_template_id):
        test_template = self._template_service.get_test_template_by_id(test_template_id)
        question_instances = [QuestionInstance(name=x.name,
                                               time_limit=x.time_limit,
                                               description=x.description,
                                               parent_id=x.id,
                                               parent_version=x.version,
                                               solution_code_snippet=clone_code_snippet(x.solution_code_snippet))
                              for x in test_template.questions]
        test_instance = TestInstance(name=test_template.name,
                                     time_limit=test_template.time_limit,
                                     questions=question_instances)
        self.db.add(test_instance)
        self.db.commit()
        return test_instance.id

    def get_test_instance(self, test_instance_id):
        # type: ()-> TestInstance
        return self.db.query(TestInstance) \
            .options(joinedload(TestInstance.questions)) \
            .filter(TestInstance.id == test_instance_id) \
            .first()

    def get_instances(self):
        return self.db.query(TestInstance) \
            .options(joinedload(TestInstance.questions)) \
            .all()

    def update_test_instance(self, test_instance_id, test_instance_update):
        # type: (int, TestInstanceUpdate)-> TestInstance

        db_test_instance = self.get_test_instance(test_instance_id)
        db_test_instance.available_after = test_instance_update.available_after
        db_test_instance.disabled_after = test_instance_update.disabled_after
        db_test_instance.time_limit = test_instance_update.time_limit
        self.db.commit()
        return db_test_instance
