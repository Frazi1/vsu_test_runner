import inspect
from functools import wraps


class BaseController(object):
    def __init__(self, bottle_app, logger, route_prefix=None):
        self.app = bottle_app
        self.logger = logger
        self._route_prefix = route_prefix
        self._register_routes()

    def _register_routes(self):
        methods = inspect.getmembers(self, lambda a: inspect.ismethod(a))
        public_methods = [m for m in methods if not (m[0].startswith("_"))]

        ctrl_name = type(self).__name__

        self.logger.info(
            "======================================================\n"
            "Controller: '{}', found endpoints: '{}'".format(ctrl_name, ", ".join(x[0] for x in public_methods)))

        for name_method in public_methods:
            try:
                name_method[1](self)
                self.logger.info("Controller: '{}', register endpoint: '{}'".format(ctrl_name, name_method[0]))
            except Exception, e:
                self.logger.error("Tried to execute:{}".format(name_method[0]), e)
        self.logger.info("======================================================\n")

    @staticmethod
    def _merge_args(kwargs, request_body_schema, response_schema, query):
        kwargs['request_body_schema'] = request_body_schema
        kwargs['response_schema'] = response_schema
        kwargs['query'] = query

    @staticmethod
    def get(route, request_body_schema=None, response_schema=None, query=None, *args, **kwargs):
        BaseController._merge_args(kwargs, request_body_schema, response_schema, query)
        return BaseController._register_route(lambda app: app.get, route, *args, **kwargs)

    @staticmethod
    def post(route, request_body_schema=None, response_schema=None, query=None, *args, **kwargs):
        BaseController._merge_args(kwargs, request_body_schema, response_schema, query)
        return BaseController._register_route(lambda app: app.post, route, *args, **kwargs)

    @staticmethod
    def put(route, request_body_schema=None, response_schema=None, query=None, *args, **kwargs):
        BaseController._merge_args(kwargs, request_body_schema, response_schema, query)
        return BaseController._register_route(lambda app: app.put, route, *args, **kwargs)

    @staticmethod
    def delete(route, request_body_schema=None, response_schema=None, query=None, *args, **kwargs):
        BaseController._merge_args(kwargs, request_body_schema, response_schema, query)
        return BaseController._register_route(lambda app: app.delete, route, *args, **kwargs)

    @staticmethod
    def _register_route(router_provider, route, *args, **kwargs):
        route = route.rstrip('/')

        def inner_decorator(func):
            @wraps(inner_decorator)
            def wrapper(self, *wa, **wkwargs):
                result_route = route

                if self._route_prefix:
                    result_route = self._route_prefix.rstrip('/') + '/' + result_route

                kwargs['_controller_instance'] = self
                router = router_provider(self.app)(result_route, *args, **kwargs)
                router(func)

            return wrapper

        return inner_decorator
