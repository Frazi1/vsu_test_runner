from __future__ import annotations
from typing import List


from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from models import Base
from models.db_group import DbGroup
from models.user_type_enum import UserTypeEnum

from models.associations import user_to_groups_association


class DbUser(Base):
    __tablename__ = "user"

    id: int = Column(Integer, primary_key=True)
    first_name: str = Column(String(255))
    middle_name: str = Column(String(255))
    last_name: str = Column(String(255), nullable=False)
    type: UserTypeEnum = Column(Enum(UserTypeEnum), nullable=False)
    groups: List[DbGroup] = relationship("DbGroup", secondary=user_to_groups_association, back_populates="users")
