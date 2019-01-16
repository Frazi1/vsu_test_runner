# coding=utf-8
import os

from bottle import Bottle, run, request, response
from bottle_sqlalchemy import SQLAlchemyPlugin

from src.db_config import ENGINE
from src.dtos.dtos import TestTemplateDto
from src.dtos.schemas import *
from src.helpers import load_modules
from src.models import Base
from src.plugins import JsonPlugin, EnableCors, BodyParser
from src.services.TemplatesService import TemplatesServiceInstance
from src.services.CodeExecuterService import executor


app = Bottle(autojson=False)
app.install(SQLAlchemyPlugin(engine=ENGINE, metadata=Base.metadata, commit=True, create=False))
# app.install(JsonPlugin())
app.install(EnableCors())
app.install(BodyParser(encode_with_json_by_default=True))

@app.route('/<:re:.*>', method='OPTIONS')
def cors():
    print 'After request hook.'
    response.headers['Access-Control-Allow-Origin'] = '*'


@app.get('/template', response_schema=TestTemplateSchema(many=True))
def get_test_templates(db):
    return TemplatesServiceInstance.get_test_templates(db)


@app.post('/template', accept_body_schema=TestTemplateSchema())
def add_test_template(db, parsed_body):
    test = parsed_body
    TemplatesServiceInstance.add_test_template(db, test)
    return test.id


@app.get('/template/<id:int>', response_schema=TestTemplateSchema())
def get_test_template_by_id(db, id):
    res = TemplatesServiceInstance.get_template_by_id(db, id)
    return res


@app.get('/languages')
def supported_languages():
    return [e.name for e in executor.get_supported_languages()]


if __name__ == "__main__":
    code_runner = os.path.join(os.path.dirname(__file__), "coderunner")
    load_modules(code_runner, "src.coderunner")
    run(app, host='localhost', port=8080, reloader=True, debug=True)
