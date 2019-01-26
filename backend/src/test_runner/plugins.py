# import ujson as json
import json as json
from functools import wraps

from bottle import response, request

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