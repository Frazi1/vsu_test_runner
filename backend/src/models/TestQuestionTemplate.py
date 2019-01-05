from sqlalchemy import *

from src.models import Base


class TestQuestionTemplate(Base):
    __tablename__ = "test_question_template"

    def __init__(self, name, description=None, time_limit=None):
        self.name = name
        self.description = description
        self.time_limit = time_limit

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text, nullable=True)
    time_limit = Column(Integer, nullable=True)

    def __repr__(self):
        return "<TestQuestionTemplate(id='{}', name='{}', description='{}', time_limit='{}'".format(self.id,
                                                                                                    self.name,
                                                                                                    self.description,
                                                                                                    self.time_limit)
