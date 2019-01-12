from functools import wraps
from bottle import response

# import ujson as json
import json as json

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
