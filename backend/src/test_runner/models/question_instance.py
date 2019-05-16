from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from typing import List

from models import Base
from models.associations import test_instance_to_question_instance_association
from models.code_snippet import CodeSnippet
from models.test_instance import TestInstance

if TYPE_CHECKING:
    from models.question_answer import QuestionAnswer


class QuestionInstance(Base):
    __tablename__ = "question_instance"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=100))
    time_limit: int = Column(Integer, nullable=True)
    description: str = Column(Text, nullable=True)

    tests: List[TestInstance] = relationship(
        "TestInstance",
        secondary=test_instance_to_question_instance_association,
        back_populates="questions"
    )

    parent_version: int = Column(BigInteger, nullable=False)
    answers: List[QuestionAnswer] = relationship("QuestionAnswer", back_populates="question_instance")
    solution_code_snippet: CodeSnippet = relationship("CodeSnippet", uselist=False)

    solution_code_snippet_id: int = Column(Integer, ForeignKey("code_snippet.id"), nullable=False)
    parent_id: int = Column(Integer, ForeignKey('test_question_template.id'), nullable=False)
