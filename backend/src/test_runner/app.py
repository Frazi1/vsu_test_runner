# coding=utf-8
import json
import os

from gevent import monkey

from controllers.instance_controller import InstanceController
from controllers.run_controller import RunController
from controllers.template_controller import TemplateController
from logger.console_logger import ConsoleLogger
from services.instance_service import InstanceService
from services.run_service import RunService

monkey.patch_all()

from bottle import Bottle, run, response
from bottle_sqlalchemy import SQLAlchemyPlugin

from db_config import ENGINE
from utils.helpers import load_modules
from models import Base
from models.argument_type import ArgumentType
from plugins import EnableCors, BodyParser, ControllerPlugin
from services.code_executer_service import executor
from services.template_service import TemplateService

app = Bottle(autojson=False)
# app.install(JsonPlugin())
app.install(EnableCors())
app.install(SQLAlchemyPlugin(engine=ENGINE, metadata=Base.metadata, commit=True, create=False))
app.install(BodyParser(encode_with_json_by_default=True))
app.install(ControllerPlugin())


def init_services():
    template_service = TemplateService()
    instance_service = InstanceService(template_service)
    run_service = RunService(instance_service)
    return [template_service, instance_service, run_service]


def init_controllers(app, template_service, instance_service, run_service, logger):
    template_ctrl = TemplateController(app, template_service, logger)
    instance_ctrl = InstanceController(app, instance_service, logger)
    run_ctrl = RunController(app, run_service, logger)

    return [template_ctrl, instance_ctrl, run_ctrl]


logger = ConsoleLogger()
services = init_services()
controllers = init_controllers(app,
                               next((x for x in services if isinstance(x, TemplateService))),
                               next((x for x in services if isinstance(x, InstanceService))),
                               next((x for x in services if isinstance(x, RunService))),
                               logger)


@app.error(500)
def error(err):
    a = 10
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    message_ = {"code": err.status_code,
                "exception": str(err.exception.message),
                "trace": err.traceback}
    dump = json.dumps(message_)
    return dump


@app.route('/<:re:.*>', method='OPTIONS')
def cors():
    print 'After request hook.'
    response.headers['Access-Control-Allow-Origin'] = '*'


@app.get('/languages')
def supported_languages():
    return [e.name for e in executor.get_supported_languages()]


@app.get('/code-types')
def supported_code_types():
    return ArgumentType.__members__.keys()


if __name__ == "__main__":
    code_runner = os.path.join(os.path.dirname(__file__), "coderunner")
    load_modules(code_runner, "coderunner")
    run(app,
        host='localhost',
        port=8080,
        # reloader=True,
        # debug=True,
        # server='gevent'
        )
