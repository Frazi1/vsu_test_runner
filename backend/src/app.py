from bottle import Bottle, run
from bottle_sqlalchemy import SQLAlchemyPlugin

from src.db_config import ENGINE
from src.dtos.dtos import TestTemplateDto
from src.models import Base
from src.plugins import UJsonPlugin
from src.services.TemplatesService import TemplatesServiceInstance

app = Bottle(autojson=False)
app.install(SQLAlchemyPlugin(engine=ENGINE, metadata=Base.metadata, commit=True, create=False))
app.install(UJsonPlugin())


@app.get('/test_templates')
def get_test_templates(db):
    templates = TemplatesServiceInstance.get_test_templates(db)
    return TestTemplateDto.list_of(templates)


if __name__ == "__main__":
    run(app, host='localhost', port=8080, reloader=True, debug=True)
