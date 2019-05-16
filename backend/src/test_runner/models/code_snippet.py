from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import *
from sqlalchemy.orm import relationship

from models import Base
from models.function import Function
from models.language_enum import LanguageEnum
from models.snippet_type import SnippetType

if TYPE_CHECKING:
    from models.test_question_template import TestQuestionTemplate
    from models.question_answer import QuestionAnswer


class CodeSnippet(Base):
    __tablename__ = "code_snippet"

    id: int = Column(Integer, primary_key=True)
    language: LanguageEnum = Column(Enum(LanguageEnum))
    snippet_type: SnippetType = Column(Enum(SnippetType))
    code: str = Column(Text)
    function: Function = relationship("Function", back_populates="code_snippets")

    question_template: TestQuestionTemplate = relationship("TestQuestionTemplate",
                                                           back_populates="solution_code_snippet",
                                                           uselist=False)

    question_answer: QuestionAnswer = relationship("QuestionAnswer",
                                                   back_populates="code_snippet",
                                                   uselist=False)

    function_id: int = Column(Integer, ForeignKey('function.id'), nullable=false)
