import itertools
from typing import List

from sqlalchemy.orm import Query, with_polymorphic
from sqlalchemy.orm.strategy_options import joinedload

from coderunner.function_run_plan import FunctionRunPlan
from models.function_inputs.base_function_input import BaseFunctionInput, DeclarativeFunctionInput
from models.function_inputs.declarative_input_item import DeclarativeInputItem
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

    def get_testing_inputs_by_ids(self, ids: List[int]) -> List[DeclarativeInputItem]:
        return self._db.query(DeclarativeInputItem) \
            .filter(DeclarativeInputItem.id.in_(ids)) \
            .all()

    def update_testing_input(self, function_run_plans: List[FunctionRunPlan]):
        update_dict = [
            {
                DeclarativeInputItem.id.name: plan.declarative_input_item_id,
                DeclarativeInputItem.output_value.name: plan.expected_result
            } for plan in function_run_plans
        ]
        self._db.bulk_update_mappings(DeclarativeInputItem, update_dict)

    def get_testing_input_by_function_id(self, function_id):
        # type:(int)->BaseFunctionInput
        poly = with_polymorphic(BaseFunctionInput, [DeclarativeFunctionInput])
        return self._db.query(poly) \
            .filter(BaseFunctionInput.target_function_id == function_id) \
            .first()
