from __future__ import annotations

from sqlalchemy import *
from sqlalchemy.orm import relationship
from typing import List, TYPE_CHECKING

from models import Base
from models.associations import test_template_test_question_template_association
from models.test_question_template import TestQuestionTemplate


class TestTemplate(Base):
    __tablename__ = 'test_template'

    def __init__(self, id_, name, time_limit, questions, *args, **kwargs):
        self.questions = questions
        self.time_limit = time_limit
        self.name = name
        self.id = id_
        super(TestTemplate, self).__init__(*args, **kwargs)

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=100))
    time_limit: int = Column(Integer, nullable=True)
    is_deleted: bool = Column(Boolean, server_default=text("FALSE"))
    questions: List[TestQuestionTemplate] = relationship(
        "TestQuestionTemplate",
        secondary=test_template_test_question_template_association,
    )

    def __repr__(self):
        return "<TestTemplate(id='{}', name='{}', time_limit='{}', questions={})>" \
            .format(self.id,
                    self.name,
                    self.time_limit,
                    [str(x) for x in self.questions]
                    )
