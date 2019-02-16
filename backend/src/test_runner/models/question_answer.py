from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class QuestionAnswer(Base):
    __tablename__ = "question_answer"

    id = Column(Integer, primary_key=True)
    test_run = relationship("TestRun", back_populates="question_answers")
    question_instance = relationship("QuestionInstance", back_populates="answers")
    code_snippet = relationship("CodeSnippet", back_populates="question_answer")

    test_run_id = Column(Integer, ForeignKey('test_run.id'))
    question_instance_id = Column(Integer, ForeignKey('question_instance.id'))
    code_snippet_id = Column(Integer, ForeignKey('code_snippet.id'))