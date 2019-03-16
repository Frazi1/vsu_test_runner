from datetime import datetime
from typing import List

from sqlalchemy.orm import joinedload, raiseload, Query

from dtos.dtos import TestRunAnswerUpdateDto
from models.code_snippet import CodeSnippet
from models.function import Function
from models.question_answer import QuestionAnswer
from models.question_instance import QuestionInstance
from models.test_instance import TestInstance
from models.test_run import TestRun
from services.base_service import BaseService
from services.code_executer_service import CodeExecuterService
from services.instance_service import InstanceService


class RunService(BaseService):

    def __init__(self,
                 instance_service,  # type: InstanceService
                 code_executer_service  # type: CodeExecuterService
                 ):
        super(RunService, self).__init__()
        self._instance_service = instance_service
        self._code_executer_service = code_executer_service

    def get_active_test_run(self, test_run_id):
        # type: (int) -> TestRun
        return self._test_run_query() \
            .filter(TestRun.id == test_run_id) \
            .first()

    def get_all_active_test_runs(self):
        # type: () -> List[TestRun]
        return self._test_run_query().all()

    def _test_run_query(self):
        # type:() -> Query
        return self._db.query(TestRun) \
            .options(
            joinedload(TestRun.question_answers)
                .joinedload(QuestionAnswer.question_instance)
                .joinedload(QuestionInstance.solution_code_snippet),
            joinedload(TestRun.question_answers)
                .joinedload(QuestionAnswer.code_snippet)
                .joinedload(CodeSnippet.function)
                .joinedload(Function.arguments),
            joinedload(TestRun.test_instance),
            raiseload('*'))

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

    def update_test_run_answers(self, test_run_id, update_dtos):
        # type: (int, List[TestRunAnswerUpdateDto]) -> None

        db_test_run = self.get_active_test_run(test_run_id)
        for update in update_dtos:
            db_answer = next((x for x in db_test_run.question_answers if x.id == update.answer_id), None)

            if not db_answer.code_snippet:
                db_answer.code_snippet = CodeSnippet()
                db_answer.code_snippet.function_id = db_answer.question_instance.solution_code_snippet.function_id

            db_answer.code_snippet.code = update.answer_code_snippet.code
            db_answer.code_snippet.language = update.answer_code_snippet.language

        self._db.commit()

    def finish_test_run(self, test_run_id, update_dtos):
        # type: (int, List[TestRunAnswerUpdateDto]) -> None
        if update_dtos:
            self.update_test_run_answers(test_run_id, update_dtos)
        db_test_run = self.get_active_test_run(test_run_id)

        validation_results = [
            self._code_executer_service.run_testing_set(answer.code_snippet, answer.code_snippet.function) for
            answer in db_test_run.question_answers
        ]

        for index in range(0, len(validation_results)):
            answer_results_mapping = validation_results[index]

            answer = db_test_run.question_answers[index]
            answer.is_validated = True
            answer.validation_passed = all((x[0] for x in answer_results_mapping))

        db_test_run.finished_at = datetime.now()
        self._db.commit()

    def get_finished_test_runs(self, user_id=None):
        # type:(int|None)-> List[TestRun]
        query = self._test_run_query().filter(TestRun.finished_at != None)
        if user_id is not None:
            pass  # Todo: filter by user id
        return query.all()

    def get_finished_run_by_id(self, run_id: int, user_id: int = None) -> TestRun:
        query = self._test_run_query().filter(TestRun.id == run_id)
        if user_id is not None:
            pass  # Todo: filter by user id
        return query.first()
