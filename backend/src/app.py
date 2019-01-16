# coding=utf-8
import os

from bottle import Bottle, run, response
from bottle_sqlalchemy import SQLAlchemyPlugin

from src.db_config import ENGINE
from src.dtos.schemas import *
from src.helpers import load_modules
from src.models import Base
from src.plugins import EnableCors, BodyParser
from src.services.CodeExecuterService import executor
from src.services.TemplatesService import TemplatesServiceInstance

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


if __name__ == "__main__":
    code_runner = os.path.join(os.path.dirname(__file__), "coderunner")
    load_modules(code_runner, "src.coderunner")
    run(app, host='localhost', port=8080, reloader=True, debug=True)
