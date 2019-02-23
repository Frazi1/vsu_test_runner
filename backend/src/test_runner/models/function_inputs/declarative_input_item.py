from sqlalchemy import Column, Integer, Text, true, ForeignKey
from sqlalchemy.orm import relationship
from typing import List

from models import Base
from models.function_inputs.declarative_input_argument_item import DeclarativeInputArgumentItem


class DeclarativeInputItem(Base):
    __tablename__ = 'declarative_input_item'

    id = Column(Integer, primary_key=True)  # type: int

    argument_items = relationship("DeclarativeInputArgumentItem",
                                  back_populates='declarative_input_item')  # type: List[DeclarativeInputArgumentItem]
    output_value = Column(Text, nullable=true)  # type: str

    declarative_function_input = relationship("DeclarativeFunctionInput",
                                              back_populates='items')  # type: 'DeclarativeFunctionInput'

    declarative_function_input_id = Column(Integer, ForeignKey('function_input.id'))  # type: int
