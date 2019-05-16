from __future__ import annotations

from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship

from models import Base
from models.code_snippet import CodeSnippet
from models.function_inputs.code_run_iteration import CodeRunIteration
from models.question_instance import QuestionInstance
from models.test_run import TestRun


class QuestionAnswer(Base):
    __tablename__ = "question_answer"

    id: int = Column(Integer, primary_key=True)
    test_run: TestRun = relationship("TestRun", back_populates="question_answers")
    question_instance: QuestionInstance = relationship("QuestionInstance",
                                                       back_populates="answers")
    code_snippet: CodeSnippet = relationship("CodeSnippet", back_populates="question_answer")
    is_validated: bool = Column(Boolean, server_default=text("FALSE"))
    validation_passed: bool = Column(Boolean, nullable=True)
    answer_iteration_results: List[CodeRunIteration] = relationship("CodeRunIteration",
                                                                    back_populates='question_answer',
                                                                    cascade="delete,delete-orphan",
                                                                    single_parent=True)

    test_run_id: int = Column(Integer, ForeignKey('test_run.id'))
    question_instance_id: int = Column(Integer, ForeignKey('question_instance.id'))
    code_snippet_id: int = Column(Integer, ForeignKey('code_snippet.id'))
