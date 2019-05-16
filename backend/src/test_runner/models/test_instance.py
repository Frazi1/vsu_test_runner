from __future__ import annotations
from typing import List, TYPE_CHECKING

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, text
from sqlalchemy.orm import relationship

from models import Base
from models.associations import test_instance_to_question_instance_association

if TYPE_CHECKING:
    from models.question_instance import QuestionInstance
    from models.test_run import TestRun


class TestInstance(Base):
    __tablename__ = "test_instance"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=100))
    created_at: datetime = Column(DateTime, server_default=func.now())
    available_after: datetime = Column(DateTime, nullable=True)
    disabled_after: datetime = Column(DateTime, nullable=True)
    time_limit: int = Column(Integer, nullable=True)
    is_active: bool = Column(Boolean, server_default=text('TRUE'))
    questions: List[QuestionInstance] = relationship(
        "QuestionInstance",
        secondary=test_instance_to_question_instance_association,
        back_populates="tests"
    )

    test_runs: List[TestRun] = relationship("TestRun", back_populates="test_instance")
