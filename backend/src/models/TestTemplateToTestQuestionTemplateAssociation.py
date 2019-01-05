from sqlalchemy import *

from src.models import Base

test_template_test_question_template_association = \
    Table('test_template_test_question_template_association', Base.metadata,
          Column('test_template_id', Integer, ForeignKey("test_template.id")),
          Column('test_question_template_id', Integer, ForeignKey("test_question_template.id")))
