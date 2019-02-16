from bottle import request
from sqlalchemy.orm import Session


class BaseService(object):

    @property
    def db(self):
        # type: () -> Session
        return request.environ['db']