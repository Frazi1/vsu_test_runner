from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from typing import List

from models import Base
from models.function_inputs.declarative_input_item import DeclarativeInputItem

print 'IMPORT BaseFunctionInput'


class BaseFunctionInput(Base):
    __tablename__ = 'function_input'

    id = Column(Integer, primary_key=True)  # type: int
    type = Column(String(50))  # type: str
    target_function = relationship("Function", back_populates='testing_input')  # type: 'Function'

    target_function_id = Column(Integer, ForeignKey('function.id'))  # type: int

    __mapper_args__ = {
        'polymorphic_on': type,
    }


class DeclarativeFunctionInput(BaseFunctionInput):
    items = relationship("DeclarativeInputItem",
                         back_populates='declarative_function_input')  # type: List[DeclarativeInputItem]
    __mapper_args__ = {
        'polymorphic_identity': 'declarative'
    }
