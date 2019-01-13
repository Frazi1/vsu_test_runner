from sqlalchemy import *
from sqlalchemy.orm import relationship

from src.models import Base
from src.models.TestTemplateToTestQuestionTemplateAssociation import test_template_test_question_template_association


class TestTemplate(Base):
    __tablename__ = 'test_template'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    time_limit = Column(Integer, nullable=True)
    questions = relationship(
        "TestQuestionTemplate",
        secondary=test_template_test_question_template_association,
    )

    def __repr__(self):
        return "<TestTemplate(id='{}', name='{}', time_limit='{}'".format(self.id, self.name, self.time_limit)
