from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from src.models import TestTemplate, TestQuestionTemplate, TestTemplateToTestQuestionTemplateAssociation

_models = [
    TestTemplate,
    TestQuestionTemplate,
    TestTemplateToTestQuestionTemplateAssociation
]
