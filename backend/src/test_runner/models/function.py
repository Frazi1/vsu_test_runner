
from sqlalchemy import *
from sqlalchemy.orm import relationship
from typing import List

from models import Base
from models.argument_type import ArgumentType
from models.code_snippet import CodeSnippet
from models.function_parameter import FunctionArgument


class Function(Base):
    __tablename__ = "function"

    id = Column(Integer, primary_key=True)  # type: int
    name = Column(String(100))  # type: str
    return_type = Column(Enum(ArgumentType))  # type: ArgumentType
    arguments = relationship("FunctionArgument", back_populates="function")  # type: List[FunctionArgument]
    code_snippets = relationship("CodeSnippet", back_populates="function")  # type: List[CodeSnippet]
