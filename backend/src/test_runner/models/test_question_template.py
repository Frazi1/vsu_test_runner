from sqlalchemy import Column, Integer, String, ForeignKey, Text, BigInteger, func, text
from sqlalchemy.orm import relationship

from . import Base


class TestQuestionTemplate(Base):
    __tablename__ = "test_question_template"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, default="")
    description = Column(Text, nullable=True)
    time_limit = Column(Integer, nullable=True)
    solution_function_id = Column(Integer, ForeignKey("function.id"), nullable=True)
    solution_function = relationship("Function", back_populates="question_templates")
    version = Column(BigInteger, server_default=text('1')) #TODO: increment version on update

    def __repr__(self):
        return "<TestQuestionTemplate(id='{}', name='{}', description='{}', time_limit='{}'".format(self.id,
                                                                                                    self.name,
                                                                                                    self.description,
                                                                                                    self.time_limit)
