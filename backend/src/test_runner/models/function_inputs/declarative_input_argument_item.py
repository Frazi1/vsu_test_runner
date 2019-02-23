from sqlalchemy import Column, ForeignKey, Integer, Text, false, Enum
from sqlalchemy.orm import relationship

from models import Base
from models.argument_type import ArgumentType


class DeclarativeInputArgumentItem(Base):
    __tablename__ = 'declarative_input_argument_item'

    id = Column(Integer, primary_key=True)  # type: int
    argument_index = Column(Integer, nullable=false)
    input_type = Column(Enum(ArgumentType), nullable=false)  # type: ArgumentType
    input_value = Text()  # type: str

    declarative_input_item = relationship("DeclarativeInputItem",
                                          back_populates='argument_items')  # type: 'DeclarativeInputItem'

    declarative_input_item_id = Column(Integer, ForeignKey('declarative_input_item.id'), nullable=false)  # type: int
