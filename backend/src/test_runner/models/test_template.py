from sqlalchemy import *
from sqlalchemy.orm import relationship

from models import Base
from models.associations import test_template_test_question_template_association


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
        return "<TestTemplate(id='{}', name='{}', time_limit='{}', questions={})>" \
            .format(self.id,
                    self.name,
                    self.time_limit,
                    [str(x) for x in self.questions])
