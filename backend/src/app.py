import os

from bottle import Bottle, run
from bottle_sqlalchemy import SQLAlchemyPlugin

from src.db_config import ENGINE
from src.dtos.dtos import TestTemplateDto
from src.helpers import load_modules
from src.models import Base
from src.plugins import JsonPlugin
from src.services.TemplatesService import TemplatesServiceInstance
from src.services.CodeExecuterService import executor

app = Bottle(autojson=False)
app.install(SQLAlchemyPlugin(engine=ENGINE, metadata=Base.metadata, commit=True, create=False))
app.install(JsonPlugin())


@app.get('/test_templates')
def get_test_templates(db):
    templates = TemplatesServiceInstance.get_test_templates(db)
    return TestTemplateDto.list_of(templates)


@app.get('/languages')
def supported_languages():
    return [e.name for e in executor.get_supported_languages()]



if __name__ == "__main__":
    code_runner = os.path.join(os.path.dirname(__file__), "coderunner")
    load_modules(code_runner, "src.coderunner")
    run(app, host='localhost', port=8080, reloader=True, debug=True)
