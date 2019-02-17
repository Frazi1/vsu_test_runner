from bottle import request
from sqlalchemy.orm import Session


class BaseService(object):

    @property
    def _db(self):
        # type: () -> Session
        return request.environ['db']