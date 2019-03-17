from sqlalchemy import *
from sqlalchemy.orm import relationship

from models import Base
from models.function import Function
from models.language_enum import LanguageEnum
from models.snippet_type import SnippetType


class CodeSnippet(Base):
    __tablename__ = "code_snippet"

    id = Column(Integer, primary_key=True)  # type: int
    language = Column(Enum(LanguageEnum))  # type: LanguageEnum
    snippet_type: SnippetType = Column(Enum(SnippetType))
    code = Column(Text)  # type: str
    function = relationship("Function", back_populates="code_snippets")  # type: Function

    question_template = relationship("TestQuestionTemplate",
                                     back_populates="solution_code_snippet",
                                     uselist=False)  # type: "TestQuestionTemplate"

    question_answer = relationship("QuestionAnswer",
                                   back_populates="code_snippet",
                                   uselist=False)  # type: "QuestionAnswer"

    function_id = Column(Integer, ForeignKey('function.id'), nullable=false)
