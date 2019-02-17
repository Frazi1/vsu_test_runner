# coding=utf-8
import json
import os

from gevent import monkey

from coderunner.python_runner import PythonRunner
from controllers.code_execution_controller import CodeExecutionController
from controllers.instance_controller import InstanceController
from controllers.run_controller import RunController
from controllers.template_controller import TemplateController
from logger.console_logger import ConsoleLogger
from services.function_service import FunctionService
from services.instance_service import InstanceService
from services.run_service import RunService

monkey.patch_all()

from bottle import Bottle, run, response

from db_config import ENGINE
from utils.helpers import load_modules
from plugins import EnableCors, BodyParser, ControllerPlugin, SQLAlchemySessionPlugin
from services.code_executer_service import CodeExecuterService
from services.template_service import TemplateService

app = Bottle(autojson=False)
# app.install(JsonPlugin())
app.install(EnableCors())
# app.install(SQLAlchemyPlugin(engine=ENGINE, metadata=Base.metadata, commit=True, create=False))
app.install(SQLAlchemySessionPlugin(engine=ENGINE, commit=True, create_session_by_default=True))
app.install(BodyParser(encode_with_json_by_default=True))
app.install(ControllerPlugin())


def _init_services():
    template_service = TemplateService()
    instance_service = InstanceService(template_service)
    run_service = RunService(instance_service)
    function_service = FunctionService()
    code_execution_service = CodeExecuterService(function_service)
    return [template_service, instance_service, run_service, code_execution_service, function_service]


def _init_controllers(app, template_service, instance_service, run_service, logger, code_execution_service):
    template_ctrl = TemplateController(app, template_service, logger)
    instance_ctrl = InstanceController(app, instance_service, logger)
    run_ctrl = RunController(app, run_service, logger)
    code_execution_ctrl = CodeExecutionController(app, logger, code_execution_service)

    return [template_ctrl, instance_ctrl, run_ctrl, code_execution_ctrl]


def _init_code_runners(code_execution_service):
    runners = [PythonRunner()]
    for r in runners:
        code_execution_service.register_runner(r)


_logger = ConsoleLogger()
_services = _init_services()
_controllers = _init_controllers(app,
                                 next((x for x in _services if isinstance(x, TemplateService))),
                                 next((x for x in _services if isinstance(x, InstanceService))),
                                 next((x for x in _services if isinstance(x, RunService))),
                                 _logger,
                                 next((x for x in _services if isinstance(x, CodeExecuterService)))
                                 )
_code_executer_service = next((x for x in _services if isinstance(x, CodeExecuterService)))
_init_code_runners(_code_executer_service)


@app.error(500)
def error(err):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    message_ = {"code": err.status_code,
                "exception": str(err.exception.message),
                "message": str(err.exception.message),
                "trace": err.traceback}
    dump = json.dumps(message_)
    return dump


@app.route('/<:re:.*>', method='OPTIONS')
def cors():
    print 'After request hook.'
    response.headers['Access-Control-Allow-Origin'] = '*'




if __name__ == "__main__":
    code_runner = os.path.join(os.path.dirname(__file__), "coderunner")
    load_modules(code_runner, "coderunner")
    run(app,
        host='localhost',
        port=8080,
        # reloader=True,
        debug=True,
        # server='gevent'
        )
