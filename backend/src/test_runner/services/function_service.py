from sqlalchemy.orm import joinedload, raiseload

from models.function import Function
from services.base_service import BaseService


class FunctionService(BaseService):
    def get_function_by_id(self, function_id):
        # type: (int) -> Function

        return self._db.query(Function) \
            .options(joinedload(Function.arguments), raiseload('*')) \
            .filter(Function.id == function_id) \
            .first()
