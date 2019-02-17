from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models import Base
from models.code_snippet import CodeSnippet
from models.question_instance import QuestionInstance
from models.test_run import TestRun


class QuestionAnswer(Base):
    __tablename__ = "question_answer"

    id = Column(Integer, primary_key=True) # type: int
    test_run = relationship("TestRun", back_populates="question_answers")  # type: TestRun
    question_instance = relationship("QuestionInstance", back_populates="answers")  # type: QuestionInstance
    code_snippet = relationship("CodeSnippet", back_populates="question_answer")  # type: CodeSnippet

    test_run_id = Column(Integer, ForeignKey('test_run.id'))
    question_instance_id = Column(Integer, ForeignKey('question_instance.id'))
    code_snippet_id = Column(Integer, ForeignKey('code_snippet.id'))
