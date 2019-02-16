from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship

from models import Base
from models.associations import test_instance_to_question_instance_association


class QuestionInstance(Base):
    __tablename__ = "question_instance"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    time_limit = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    tests = relationship(
        "TestInstance",
        secondary=test_instance_to_question_instance_association,
        back_populates="questions"
    )
    parent_id = Column(Integer, ForeignKey('test_question_template.id'), nullable=False)
    parent_version = Column(BigInteger, nullable=False)
    answers = relationship("QuestionAnswer", back_populates="question_instance")
    solution_code_snippet_id = Column(Integer, ForeignKey("code_snippet.id"), nullable=False)
    solution_code_snippet = relationship("CodeSnippet", uselist=False)