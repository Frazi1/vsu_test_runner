# coding=utf-8
import json
import os
import docker
from typing import List

import bottle
from bottle import Bottle, run, response, request
from gevent import monkey

from app_config import Config, ContainerType
from coderunner.csharp import charp_docker_runner
from coderunner.csharp.charp_docker_runner import CSharpDockerRunner
from coderunner.csharp.csharp_runner import CSharpRunner
from coderunner.python.python_runner import PythonRunner
from controllers.code_execution_controller import CodeExecutionController
from controllers.finished_run_controller import FinishedRunController
from controllers.function_testing_controller import FunctionTestingController
from controllers.instance_controller import InstanceController
from controllers.run_controller import RunController
from controllers.template_controller import TemplateController
from db_config import ENGINE
from interfaces.service_resolver import ServiceResolver
from logger.console_logger import ConsoleLogger
from models.argument_type import ArgumentType
from models.language_enum import LanguageEnum
from plugins import EnableCors, BodyParser
from services.code_executer_service import CodeExecuterService
from services.function_service import FunctionService
from services.instance_service import InstanceService
from services.run_service import RunService
from services.template_service import TemplateService
from services.testing_input_service import TestingInputService
from utils.bottle_controller_plugin.controller_plugin import ControllerPlugin, BaseController
from utils.bottle_pyjson_plugin.pyjson_plugin import BottlePyJsonPlugin
from utils.bottle_query_parser_plugin.query_parser_plugin import QueryParamParserPlugin
from utils.business_error import BusinessException
from utils.helpers import load_modules
from utils.pyjson.pyjson import PyJsonStrategy, PyJsonConverter
from utils.bottle_sqlalchemy_session_manager_plugin.bottle_sqlalchemy_session_manager_plugin import \
    BottleSQLAlchemySessionPlugin
import utils.validation_utils as validation

monkey.patch_all()


class ArgumentTypeStrategy(PyJsonStrategy):
    target_type = ArgumentType

    def to_json(self, value):
        return {"name": value.name}

    def from_json(self, value, concrete_type=None):
        val = value["name"]
        validation.is_not_none(val, "val")
        return concrete_type[val]


class LanguageStrategy(PyJsonStrategy):
    target_type = LanguageEnum

    def to_json(self, value):
        return {"name": value.name}

    def from_json(self, value, concrete_type=None):
        name_ = value["name"]
        return concrete_type[name_]


def _init_services():
    logger = ConsoleLogger()
    testing_input_service = TestingInputService()
    function_service = FunctionService(testing_input_service)
    code_execution_service = CodeExecuterService(function_service, testing_input_service)
    template_service = TemplateService(code_execution_service)
    instance_service = InstanceService(template_service)
    run_service = RunService(instance_service, code_execution_service)

    return ServiceResolver(logger,
                           code_execution_service,
                           function_service,
                           instance_service,
                           run_service,
                           template_service,
                           testing_input_service)


_service_resolver = _init_services()

enable_cors_plugin = EnableCors()
session_plugin = BottleSQLAlchemySessionPlugin(engine=ENGINE, commit=False, create_session_by_default=True)
body_parser = BodyParser(encode_with_json_by_default=True)
controller_plugin = ControllerPlugin()
query_param_parser_plugin = QueryParamParserPlugin()
converter = PyJsonConverter([ArgumentTypeStrategy(), LanguageStrategy()], logger=_service_resolver.logger)
bottle_py_json_plugin = BottlePyJsonPlugin(pyjson_converter=converter)

app = Bottle(autojson=False)
# app.install(JsonPlugin())
app.install(enable_cors_plugin)
# app.install(SQLAlchemyPlugin(engine=ENGINE, metadata=Base.metadata, commit=True, create=False))
app.install(session_plugin)
app.install(body_parser)
app.install(controller_plugin)
app.install(query_param_parser_plugin)
app.install(bottle_py_json_plugin)

app_config = Config()

bottle.BaseRequest.MEMFILE_MAX = 4 * 1024 * 1024


def _init_controllers(app, service_resolver):
    # type: (Bottle, ServiceResolver) -> List[BaseController]

    template_ctrl = TemplateController(app, service_resolver.template_service, service_resolver.logger)

    instance_ctrl = InstanceController(app, service_resolver.instance_service, service_resolver.logger)

    run_ctrl = RunController(app, service_resolver.run_service, service_resolver.logger)

    code_execution_ctrl = CodeExecutionController(app,
                                                  service_resolver.logger,
                                                  service_resolver.code_executer_service,
                                                  service_resolver.function_service)

    function_testing_ctrl = FunctionTestingController(app, service_resolver)

    finished_run_controller = FinishedRunController(app, service_resolver)

    return [template_ctrl, instance_ctrl, run_ctrl, code_execution_ctrl, function_testing_ctrl, finished_run_controller]


def _init_code_runners(code_execution_service):
    runners = [
        PythonRunner(app_config),
        CSharpRunner(app_config) if app_config.CONTAINER_TYPE == ContainerType.Native else CSharpDockerRunner(
            app_config, docker.from_env())
    ]
    for r in runners:
        code_execution_service.register_runner(r)


_controllers = _init_controllers(app, _service_resolver)
_code_executer_service = _service_resolver.code_executer_service
_init_code_runners(_code_executer_service)


@app.error(500)
def error(err):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    if err is BusinessException:
        message_ = {"error": str(err)}
        response.status = 400
    else:
        message_ = {"code": err.status_code,
                    "exception": str(err.exception),
                    "message": str(err.exception),
                    "trace": err.traceback}

    dump = json.dumps(message_)
    return dump


@app.hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


@app.route('/<:re:.*>', method='OPTIONS')
def cors():
    print('After request hook.')
    response.headers['Access-Control-Allow-Origin'] = '*'


@app.route('/app',
           skip=[body_parser, bottle_py_json_plugin, session_plugin, query_param_parser_plugin, controller_plugin])
def frontend_main():
    return bottle.static_file('index.html', root='static')

@app.route('/app/<filepath:re:.+>',
           skip=[body_parser, bottle_py_json_plugin, session_plugin, query_param_parser_plugin, controller_plugin])
def frontend(filepath):
    return bottle.static_file(filepath, root='static')


if __name__ == "__main__":
    code_runner = os.path.join(os.path.dirname(__file__), "coderunner")
    load_modules(code_runner, "coderunner")
    dtos = os.path.join(os.path.dirname(__file__), "dtos")
    load_modules(dtos, "dtos")
    run(app,
        host='localhost',
        port=8080,
        # reloader=True,
        debug=True,
        # server='gevent'
        )
