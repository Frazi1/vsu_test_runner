from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from src.models import TestTemplate, TestQuestionTemplate, TestTemplateToTestQuestionTemplateAssociation, Function, \
    FunctionParameter, CodeSnippet

_models = [
    TestTemplate,
    TestQuestionTemplate,
    TestTemplateToTestQuestionTemplateAssociation,
    Function,
    FunctionParameter,
    CodeSnippet
]
