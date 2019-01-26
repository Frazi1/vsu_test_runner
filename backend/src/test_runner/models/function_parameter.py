from sqlalchemy import *
from sqlalchemy.orm import relationship

from models import Base
from models.argument_type import ArgumentType


class FunctionParameter(Base):
    __tablename__ = "function_parameter"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(ArgumentType), nullable=False)
    name = Column(String(100), nullable=False, default="")
    function_id = Column(Integer, ForeignKey('function.id'), nullable=false)
    function = relationship("Function", back_populates="parameters")

    def __init__(self, type_, name):
        self.type = type_
        self.name = name
