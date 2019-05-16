from __future__ import annotations
from typing import TYPE_CHECKING

from typing import List

from sqlalchemy import *
from sqlalchemy.orm import relationship

from models import Base
from models.argument_type import ArgumentType
from models.function_inputs.base_function_input import BaseFunctionInput
from models.function_parameter import FunctionArgument

if TYPE_CHECKING:
    from models.code_snippet import CodeSnippet


class Function(Base):
    __tablename__ = "function"

    def __init__(self, id, name, return_type, arguments, testing_input, *args, **kwargs):
        self.id = id
        self.name = name
        self.return_type = return_type
        self.arguments = arguments
        self.testing_input = testing_input
        super(Function, self).__init__(*args, **kwargs)

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(100))
    return_type: ArgumentType = Column(Enum(ArgumentType))
    arguments: List[FunctionArgument] = relationship("FunctionArgument", back_populates="function")
    code_snippets: List[CodeSnippet] = relationship("CodeSnippet", back_populates="function")
    testing_input: BaseFunctionInput = relationship("BaseFunctionInput", back_populates="target_function",
                                                    uselist=False)
