from __future__ import annotations
from typing import List, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models import Base

from models.associations import user_to_groups_association
if TYPE_CHECKING:
    from models.db_user import DbUser


class DbGroup(Base):
    __tablename__ = "group"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(255), nullable=False)
    description: str = Column(String(255))

    parent_id: int = Column(Integer, ForeignKey('group.id'))
    parent: DbGroup = relationship("DbGroup", back_populates="children")
    children: List[DbGroup] = relationship("DbGroup", back_populates="parent")

    users: List[DbUser] = relationship("DbUser", secondary=user_to_groups_association, back_populates="groups")
