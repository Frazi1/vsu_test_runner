from sqlalchemy.orm import Query, with_polymorphic
from sqlalchemy.orm.strategy_options import joinedload

from models.function_inputs.base_function_input import BaseFunctionInput, DeclarativeFunctionInput
from services.base_service import BaseService


class TestingInputService(BaseService):

    def _full(self, query):
        # type: (Query) -> Query
        return query.options(joinedload(query.DeclarativeFunctionInput.items))

    def get_function_input_by_id(self, id_):
        # type:(int)->BaseFunctionInput
        return self._full(self._db.query(BaseFunctionInput)) \
            .filter(BaseFunctionInput.id == id_) \
            .first()

    def get_testing_input_by_function_id(self, function_id):
        # type:(int)->BaseFunctionInput
        poly = with_polymorphic(BaseFunctionInput, [DeclarativeFunctionInput])
        return self._db.query(poly) \
            .filter(BaseFunctionInput.target_function_id == function_id) \
            .first()
