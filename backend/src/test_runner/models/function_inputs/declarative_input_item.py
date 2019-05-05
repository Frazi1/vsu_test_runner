from typing import List

from sqlalchemy import Column, Integer, Text, true, ForeignKey, Boolean, text
from sqlalchemy.orm import relationship

from models import Base
from models.function_inputs.declarative_input_argument_item import DeclarativeInputArgumentItem


class DeclarativeInputItem(Base):
    __tablename__ = 'declarative_input_item'

    def __init__(self, id_=None, argument_items=None, output_value=None, predefined_output_value=False,
                 *args, **kwargs):
        self.id = id_
        self.argument_items = argument_items
        self.output_value = output_value
        self.predefined_output_value = predefined_output_value
        super(DeclarativeInputItem, self).__init__(*args, **kwargs)

    id = Column(Integer, primary_key=True)  # type: int

    argument_items = relationship("DeclarativeInputArgumentItem",
                                  back_populates='declarative_input_item', lazy="joined")  # type: List[DeclarativeInputArgumentItem]
    output_value = Column(Text, nullable=true)  # type: str
    predefined_output_value: bool = Column(Boolean, nullable=False, server_default=text('FALSE'))

    declarative_function_input = relationship("DeclarativeFunctionInput",
                                              back_populates='items')  # type: 'DeclarativeFunctionInput'
    code_run_iterations = relationship("CodeRunIteration", back_populates='iteration_template')

    declarative_function_input_id = Column(Integer, ForeignKey('function_input.id'))  # type: int
