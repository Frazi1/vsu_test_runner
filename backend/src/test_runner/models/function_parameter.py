from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import *
from sqlalchemy.orm import relationship

from models import Base
from models.argument_type import ArgumentType

if TYPE_CHECKING:
    from models.function import Function


class FunctionArgument(Base):
    __tablename__ = "function_argument"

    id: int = Column(Integer, primary_key=True)
    type: ArgumentType = Column(Enum(ArgumentType), nullable=False)
    name: str = Column(String(100), nullable=False, default="")
    function_id: int = Column(Integer, ForeignKey('function.id'), nullable=false)
    function: Function = relationship("Function", back_populates="arguments")
