from sqlalchemy import *

from models import Base
# from models.question_instance import QuestionInstance
# from models.test_instance import TestInstance

test_template_test_question_template_association = \
    Table('test_template_test_question_template_association', Base.metadata,
          Column('test_template_id', Integer, ForeignKey("test_template.id")),
          Column('test_question_template_id', Integer, ForeignKey("test_question_template.id")))

test_instance_to_question_instance_association = Table(
    'test_instance_to_question_instance_association',
    Base.metadata,
    # Column('test_instance_id', Integer, ForeignKey(TestInstance.id)),
    # Column('question_instance_id', Integer, ForeignKey(QuestionInstance.id))
    Column('test_instance_id', Integer, ForeignKey("test_instance.id")),
    Column('question_instance_id', Integer, ForeignKey("question_instance.id"))
)