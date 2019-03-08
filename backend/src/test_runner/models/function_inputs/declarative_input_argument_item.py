from sqlalchemy import Column, ForeignKey, Integer, Text, false, Enum
from sqlalchemy.orm import relationship

from models import Base
from models.argument_type import ArgumentType


class DeclarativeInputArgumentItem(Base):
    __tablename__ = 'declarative_input_argument_item'

    def __init__(self, id_=None, argument_index=None, input_type=None, input_value=None, *args, **kwargs):
        self.id = id_
        self.argument_index = argument_index
        self.input_type = input_type
        self.input_value = input_value
        super(DeclarativeInputArgumentItem, self).__init__(*args, **kwargs)

    id = Column(Integer, primary_key=True)  # type: int
    argument_index = Column(Integer, nullable=false)
    input_type = Column(Enum(ArgumentType), nullable=false)  # type: ArgumentType
    input_value = Text()  # type: str

    declarative_input_item = relationship("DeclarativeInputItem",
                                          back_populates='argument_items')  # type: 'DeclarativeInputItem'

    declarative_input_item_id = Column(Integer, ForeignKey('declarative_input_item.id'), nullable=false)  # type: int
