from typing import List

from sqlalchemy.orm import joinedload, raiseload

from coderunner.function_run_argument import FunctionRunArgument
from coderunner.function_run_plan import FunctionRunPlan
from dtos.function_testing_input_schemas import FunctionTestingInputDtoSchema
from models.function import Function
from models.function_inputs.base_function_input import DeclarativeFunctionInput
from services.base_service import BaseService
from services.testing_input_service import TestingInputService
from shared.value_converter import ValueConverter
from utils.run_plan_helpers import get_run_plans


class FunctionService(BaseService):

    def __init__(self, testing_input_service):
        # type: (TestingInputService) -> None
        super(FunctionService, self).__init__()

        self._testing_input_service = testing_input_service

    def get_function_by_id(self, function_id):
        # type: (int) -> Function

        return self._db.query(Function) \
            .options(joinedload(Function.arguments),
                     joinedload(Function.code_snippets),
                     joinedload(Function.testing_input),
                     raiseload('*')) \
            .filter(Function.id == function_id) \
            .first()

    def add_testing_input(self, function_id, testing_input):
        # type: (int, FunctionTestingInputDtoSchema) -> None
        function_object = self.get_function_by_id(function_id)
        function_object.testing_input = testing_input.declarative_input
        self._db.commit()

    def get_function_run_plans(self, function_id: int) -> List[FunctionRunPlan]:
        function_ = self.get_function_by_id(function_id)
        testing_input = self._testing_input_service.get_testing_input_by_function_id(function_id)
        return get_run_plans(function_, testing_input)