from sqlalchemy.orm import joinedload, raiseload

from dtos.function_testing_input_schemas import FunctionTestingInputDtoSchema
from models.function import Function
from services.base_service import BaseService


class FunctionService(BaseService):
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
