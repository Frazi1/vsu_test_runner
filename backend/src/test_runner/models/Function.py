from sqlalchemy import *
from sqlalchemy.orm import relationship

from models import Base
from models.argument_type import ArgumentType


class Function(Base):
    __tablename__ = "function"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    return_type = Column(Enum(ArgumentType))
    arguments = relationship("FunctionArgument", back_populates="function")
    code_snippet = relationship("CodeSnippet", uselist=False, back_populates="function")
    question_templates = relationship("TestQuestionTemplate", back_populates="solution_function")
