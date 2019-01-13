import os

from bottle import Bottle, run, request, response
from bottle_sqlalchemy import SQLAlchemyPlugin

from src.db_config import ENGINE
from src.dtos.dtos import TestTemplateDto
from src.dtos.schemas import *
from src.helpers import load_modules
from src.models import Base
from src.plugins import JsonPlugin, EnableCors
from src.services.TemplatesService import TemplatesServiceInstance
from src.services.CodeExecuterService import executor


app = Bottle(autojson=False)
app.install(SQLAlchemyPlugin(engine=ENGINE, metadata=Base.metadata, commit=True, create=False))
app.install(JsonPlugin())
app.install(EnableCors())


@app.route('/<:re:.*>', method='OPTIONS')
def cors():
    print 'After request hook.'
    response.headers['Access-Control-Allow-Origin'] = '*'

@app.get('/template')
def get_test_templates(db):
    templates = TemplatesServiceInstance.get_test_templates(db)
    return TestTemplateDto.list_of(templates)

@app.post('/template')
def add_test_template(db):
    print request.json
    var = TestTemplateSchema().load(request.json)
    print var


@app.get('/languages')
def supported_languages():
    return [e.name for e in executor.get_supported_languages()]


if __name__ == "__main__":
    code_runner = os.path.join(os.path.dirname(__file__), "coderunner")
    load_modules(code_runner, "src.coderunner")
    run(app, host='localhost', port=8080, reloader=True, debug=True)
