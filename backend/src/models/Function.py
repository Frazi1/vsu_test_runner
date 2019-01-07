from sqlalchemy import *
from sqlalchemy.orm import relationship

from src.models import Base
from src.models.ArgumentType import ArgumentType


class Function(Base):
    __tablename__ = "function"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    return_type = Column(Enum(ArgumentType))
    parameters = relationship("FunctionParameter", back_populates="function")

    def __init__(self, name, return_type, parameters):
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
