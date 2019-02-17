from sqlalchemy.orm import joinedload, raiseload
from typing import List

from models.question_answer import QuestionAnswer
from models.question_instance import QuestionInstance
from models.test_instance import TestInstance
from models.test_run import TestRun
from services.base_service import BaseService
from services.instance_service import InstanceService


class RunService(BaseService):

    def __init__(self,
                 instance_service  # type: InstanceService
                 ):
        super(RunService, self).__init__()
        self._instance_service = instance_service

    def get_active_test_run(self, test_run_id):
        # type: (int) -> TestRun
        return self._db.query(TestRun) \
            .options(joinedload(TestRun.question_answers).joinedload(QuestionAnswer.question_instance).joinedload(QuestionInstance.solution_code_snippet),
                     joinedload(TestRun.question_answers).joinedload(QuestionAnswer.code_snippet),
                     joinedload(TestRun.test_instance),
                     raiseload('*')) \
            .filter(TestRun.id == test_run_id) \
            .first()

    def start_run_from_instance(self, instance_id):
        test_instance = self._instance_service.get_test_instance(instance_id)
        test_run = TestRun(test_instance=test_instance)
        test_run.question_answers = self._create_empty_question_answers(test_instance, test_run)
        self._db.add(test_run)
        self._db.commit()
        return test_run.id

    def _create_empty_question_answers(self, test_instance, test_run):
        # type: (TestInstance, TestRun) -> List(QuestionAnswer)

        return [QuestionAnswer(test_run=test_run, question_instance=q) for q in test_instance.questions]
