from sqlalchemy import *
from sqlalchemy.orm import relationship

from models import Base
from models.argument_type import ArgumentType


class FunctionArgument(Base):
    __tablename__ = "function_argument"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(ArgumentType), nullable=False)
    name = Column(String(100), nullable=False, default="")
    function_id = Column(Integer, ForeignKey('function.id'), nullable=false)
    function = relationship("Function", back_populates="arguments")