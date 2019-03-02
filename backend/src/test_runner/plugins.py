# import ujson as json
import json as json
from functools import wraps

import bottle
from bottle import response, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession
from typing import List

from dtos.validation_exception import ValidationException


class JsonPlugin:
    api = 2

    def __init__(self):
        pass

    def setup(self, app):
        pass

    def apply(self, callback, context):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            response.content_type = "application/json; charset=utf-8"
            value = callback(*args, **kwargs)
            return json.dumps(value)

        return wrapper


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS, DELETE'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


class BodyParser(object):
    name = 'body_parser'
    api = 2

    def __init__(self, encode_with_json_by_default=False):
        self.encode_with_json_by_default = encode_with_json_by_default
        self.response_content_type = 'application/json; charset=utf-8'

    def _set_resp_content_type(self, response_):
        response_.headers['Content-Type'] = self.response_content_type

    def _add_parsed_req_body(self, callback, schema, request_):
        body = request_.json  # TODO: check is json exists
        load = schema.load(body)
        if load.errors and len(load.errors) > 0:
            raise ValidationException(load.errors)

        parsed_body = load.data

        def wrapped(*a, **ka):
            return callback(parsed_body=parsed_body, *a, **ka)

        return wrapped

    def _encode_with_json(self, callback, response_):
        self._set_resp_content_type(response_)

        def wrapped(*a, **ka):
            return json.dumps(callback(*a, **ka))

        return wrapped

    def _encode_with_schema(self, callback, schema, response_):
        self._set_resp_content_type(response_)

        def wrapped(*a, **ka):
            callback_res = callback(*a, **ka)
            dumps = schema.dumps(callback_res)
            return dumps.data

        return wrapped

    def apply(self, callback, context):
        request_body_schema = context.config.request_body_schema
        response_schema = context.config.response_schema

        def inner(*a, **ka):
            inner_callback = callback
            if request_body_schema is not None:
                inner_callback = self._add_parsed_req_body(inner_callback, request_body_schema, request)

            if response_schema is not None:
                inner_callback = self._encode_with_schema(inner_callback, response_schema, response)
            elif self.encode_with_json_by_default is True:
                inner_callback = self._encode_with_json(inner_callback, response)

            return inner_callback(*a, **ka)

        return inner


class ControllerPlugin(object):
    api = 2
    name = 'controller-plugin'

    def apply(self, callback, context):
        def inner(*a, **ka):
            controller_instance = context.config._controller_instance
            if controller_instance is None:
                return callback(*a, **ka)
            return callback(controller_instance, *a, **ka)

        return inner


class SQLAlchemySessionPlugin(object):
    api = 2
    name = 'sqlalchemy-session-plugin'

    def __init__(self, engine, create_session_by_default=True, commit=False, session_maker=None):
        self.commit = commit
        self.engine = engine
        self.create_session_by_default = create_session_by_default
        self.session_maker = session_maker or sessionmaker()

    def apply(self, callback, context):
        should_create_session = getattr(context.config, 'create_session') or self.create_session_by_default

        def wrapper(*a, **kwa):
            if should_create_session is False:
                return callback(*a, **kwa)
            session = self.session_maker(bind=self.engine)
            request.environ['db'] = session
            try:
                rv = callback(*a, **kwa)
                if self.commit:
                    session.commit()

            except (SQLAlchemyError, bottle.HTTPError):
                session.rollback()
                raise
            except bottle.HTTPResponse:
                if self.commit:
                    session.commit()
                raise
            finally:
                if isinstance(self.session_maker, ScopedSession):
                    self.session_maker.remove()
                else:
                    session.close()
                request.environ['db'] = None
            return rv

        return wrapper


class QueryParamParser(object):
    api = 2
    name = 'query_param_parser'
    type_parsers = {}

    def __init__(self, route_arg_name='query'):
        super(QueryParamParser, self).__init__()
        self.route_arg_name = route_arg_name
        self.init_parsers()

    def init_parsers(self):
        self.type_parsers[str] = lambda x: str(x)
        self.type_parsers[int] = lambda x: int(x)
        self.type_parsers[bool] = lambda x: bool_parser(x)

        def bool_parser(value):
            # type: (str | None) -> bool
            if value is None:
                return False

            lower_value = value.lower()
            if lower_value == 'true':

                return True
            if lower_value == 'false':
                return False

            raise QueryParserException("Value: '{}' is not supported.".format(value))

    def apply(self, callback, context):
        queries = getattr(context.config, self.route_arg_name)  # type: List[QueryParam]

        if queries is None:
            return callback

        def wrapper(*a, **kwa):
            for query in queries:
                value = request.query.get(query.name)
                parser = self.type_parsers.get(query.type)
                if parser is None:
                    raise QueryParserException("Parser for type '{}' is not defined.".format(str(query.type)))
                parsed_value = parser(value)

                if kwa.get(query.inject_name) is not None:
                    raise QueryParserException("Parameter '{}' cannot be injected because it already exists.".format(query.inject_name))

                kwa[query.inject_name] = parsed_value
            return callback(*a, **kwa)

        return wrapper


class QueryParam:
    def __init__(self, name, type_, inject_name=None):
        self.name = name  # type: str
        self.type = type_  # type: type
        self.inject_name = inject_name or self.name  # type: str


class QueryParserException(Exception):
    pass
