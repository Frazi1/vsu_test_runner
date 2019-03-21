from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from typing import List

from models import Base
from models.associations import test_instance_to_question_instance_association
from models.code_snippet import CodeSnippet
from models.test_instance import TestInstance


class QuestionInstance(Base):
    __tablename__ = "question_instance"

    id = Column(Integer, primary_key=True)  # type:int
    name = Column(String(length=100))  # type: str
    time_limit = Column(Integer, nullable=True)  # type: int
    description = Column(Text, nullable=True)  # type: str

    tests = relationship(
        "TestInstance",
        secondary=test_instance_to_question_instance_association,
        back_populates="questions"
    )  # type: List[TestInstance]

    parent_version = Column(BigInteger, nullable=False)  # type: int
    answers = relationship("QuestionAnswer", back_populates="question_instance")  # type: List["QuestionAnswer"]
    solution_code_snippet: CodeSnippet = relationship("CodeSnippet", uselist=False)

    solution_code_snippet_id = Column(Integer, ForeignKey("code_snippet.id"), nullable=False)  # type: int
    parent_id = Column(Integer, ForeignKey('test_question_template.id'), nullable=False)  # type: int
