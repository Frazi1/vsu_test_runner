from sqlalchemy import *
from sqlalchemy.orm import relationship
from typing import List

from models import Base
from models.associations import test_template_test_question_template_association
from models.test_question_template import TestQuestionTemplate


class TestTemplate(Base):
    __tablename__ = 'test_template'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    time_limit = Column(Integer, nullable=True)
    is_deleted = Column(Boolean, server_default=text("FALSE"))
    questions = relationship(
        "TestQuestionTemplate",
        secondary=test_template_test_question_template_association,
    ) # type: List[TestQuestionTemplate]

    def __repr__(self):
        return "<TestTemplate(id='{}', name='{}', time_limit='{}', questions={})>" \
            .format(self.id,
                    self.name,
                    self.time_limit,
                    [str(x) for x in self.questions])
