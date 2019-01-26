# coding=utf-8
import os
import json
from gevent import monkey

monkey.patch_all()

from bottle import Bottle, run, response
from bottle_sqlalchemy import SQLAlchemyPlugin

from db_config import ENGINE
from dtos.schemas import *
from helpers import load_modules
from models import Base
from models.argument_type import ArgumentType
from plugins import EnableCors, BodyParser
from services.code_executer_service import executor
from services.templates_service import TemplatesServiceInstance

app = Bottle(autojson=False)
app.install(SQLAlchemyPlugin(engine=ENGINE, metadata=Base.metadata, commit=True, create=False))
# app.install(JsonPlugin())
app.install(EnableCors())
app.install(BodyParser(encode_with_json_by_default=True))


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


@app.get('/template', response_schema=TestTemplateSchema(many=True))
def get_test_templates(db):
    return TemplatesServiceInstance.get_test_templates(db)


@app.post('/template', request_body_schema=TestTemplateSchema())
def add_test_template(db, parsed_body):
    id_ = TemplatesServiceInstance.add_test_template(db, parsed_body)
    return id_


@app.get('/template/<id:int>', response_schema=TestTemplateSchema())
def get_test_template_by_id(db, id):
    res = TemplatesServiceInstance.get_test_template_by_id(db, id)
    return res


@app.put('/template/<id:int>', request_body_schema=TestTemplateSchema(), response_schema=TestTemplateSchema())
def update_test_template(db, id, parsed_body):
    return TemplatesServiceInstance.update_test_template(db, id, parsed_body)


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
