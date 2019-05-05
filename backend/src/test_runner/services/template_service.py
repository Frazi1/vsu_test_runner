from sqlalchemy.orm import joinedload, joinedload_all

from models.code_snippet import CodeSnippet
from models.function import Function
from models.test_question_template import TestQuestionTemplate
from models.test_template import TestTemplate
from services.base_service import BaseService
from services.code_executer_service import CodeExecuterService
from utils.run_plan_helpers import get_run_plans


class TemplateService(BaseService):

    def __init__(self, code_executer_service: CodeExecuterService):
        self._code_executer_service = code_executer_service

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
        res = self._db.query(TestTemplate).options(
            joinedload_all(TestTemplate.questions, TestQuestionTemplate.solution_code_snippet, CodeSnippet.function,
                           Function.arguments),
            joinedload_all(TestTemplate.questions, TestQuestionTemplate.solution_code_snippet, CodeSnippet.function,
                           Function.testing_input)) \
            .filter(TestTemplate.id == id_) \
            .first()
        return res

    def update_test_template(self, test: TestTemplate):
        merged = self._db.merge(test)
        self._db.flush()
        return merged

    def update_test_template_and_calc_expected_results(self, db_test: TestTemplate):
        updated_test = self.update_test_template(db_test)
        for q in updated_test.questions:
            snippet: CodeSnippet = q.solution_code_snippet
            plans = get_run_plans(snippet.function, snippet.function.testing_input)
            self._code_executer_service.execute_function_tests_and_save_valid_results(
                snippet,
                snippet.function,
                plans)

        self._db.commit()

    def delete_test_template(self, id_):
        test_template = self.get_test_template_by_id(id_)
        test_template.is_deleted = True
        self._db.commit()

    def restore(self, id_):
        test_template = self.get_test_template_by_id(id_)
        test_template.is_deleted = False
        self._db.commit()
