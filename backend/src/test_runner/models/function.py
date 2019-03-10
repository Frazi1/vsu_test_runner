from sqlalchemy import *
from sqlalchemy.orm import relationship
from typing import List

from models import Base
from models.argument_type import ArgumentType
from models.function_inputs.base_function_input import BaseFunctionInput
from models.function_parameter import FunctionArgument


class Function(Base):
    __tablename__ = "function"

    def __init__(self, id, name, return_type, arguments, testing_input, *args, **kwargs):
        self.id = id
        self.name = name
        self.return_type = return_type
        self.arguments = arguments
        self.testing_input = testing_input
        super(Function,self).__init__(*args, **kwargs)

    id = Column(Integer, primary_key=True)  # type: int
    name = Column(String(100))  # type: str
    return_type = Column(Enum(ArgumentType))  # type: ArgumentType
    arguments = relationship("FunctionArgument", back_populates="function")  # type: List[FunctionArgument]
    code_snippets = relationship("CodeSnippet", back_populates="function")  # type: List[CodeSnippet]
    testing_input = relationship("BaseFunctionInput", back_populates="target_function", uselist=False)  # type: BaseFunctionInput
