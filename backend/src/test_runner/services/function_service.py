from sqlalchemy.orm import joinedload, raiseload
from typing import List

from coderunner.function_run_argument import FunctionRunArgument
from coderunner.function_run_plan import FunctionRunPlan
from dtos.function_testing_input_schemas import FunctionTestingInputDtoSchema
from models.function import Function
from models.function_inputs.base_function_input import DeclarativeFunctionInput
from services.base_service import BaseService
from services.testing_input_service import TestingInputService
from shared.value_converter import ValueConverter


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

    def get_function_run_plans(self, function_id, code, language):
        # type: (int) -> List[FunctionRunPlan]

        function_ = self.get_function_by_id(function_id)
        testing_input = self._testing_input_service.get_testing_input_by_function_id(function_id)
        if isinstance(testing_input, DeclarativeFunctionInput):
            res = [
                FunctionRunPlan(
                    language,
                    code,
                    function_, [
                        FunctionRunArgument(arg.input_type, arg.input_value) for arg in input.argument_items
                    ],
                    ValueConverter.from_string(function_.return_type, input.output_value)
                ) for input in testing_input.items]
            return res
