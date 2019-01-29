import inspect
from functools import wraps


class BaseController(object):
    def __init__(self, bottle_app, logger):
        self.app = bottle_app
        self.logger = logger
        self._register_routes()

    def _register_routes(self):
        methods = inspect.getmembers(self, lambda a: inspect.ismethod(a))
        public_methods = [m for m in methods if not (m[0].startswith("_"))]

        ctrl_name = type(self).__name__

        self.logger.info(
            "Controller: '{}', found endpoints: '{}'".format(ctrl_name, ", ".join(x[0] for x in public_methods)))

        for name_method in public_methods:
            try:
                name_method[1](self)
                self.logger.info("Controller: '{}', register endpoint: '{}'".format(ctrl_name, name_method[0]))
            except Exception, e:
                self.logger.error("Tried to execute:{}".format(name_method[0]), e)
    @staticmethod
    def get(*args, **kwargs):
        return BaseController._register_route(lambda app: app.get, *args, **kwargs)

    @staticmethod
    def post(*args, **kwargs):
        return BaseController._register_route(lambda app: app.post, *args, **kwargs)

    @staticmethod
    def put(*args, **kwargs):
        return BaseController._register_route(lambda app: app.put, *args, **kwargs)

    @staticmethod
    def delete(*args, **kwargs):
        return BaseController._register_route(lambda app: app.delete, *args, **kwargs)

    @staticmethod
    def _register_route(router_provider, *args, **kwargs):
        def inner_decorator(func):
            @wraps(inner_decorator)
            def wrapper(self, *wa, **wkwargs):
                kwargs['_controller_instance'] = self
                router = router_provider(self.app)(*args, **kwargs)
                router(func)

            return wrapper

        return inner_decorator
