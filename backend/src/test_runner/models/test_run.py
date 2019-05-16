from __future__ import annotations
from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from models import Base
from models.test_instance import TestInstance

if TYPE_CHECKING:
    from models.question_answer import QuestionAnswer


class TestRun(Base):
    __tablename__ = "test_run"

    id: int = Column(Integer, primary_key=True)
    test_instance: TestInstance = relationship("TestInstance", back_populates="test_runs")
    question_answers: List[QuestionAnswer] = relationship("QuestionAnswer", back_populates="test_run")
    started_at: datetime = Column(DateTime, server_default=func.now())
    finished_at: datetime = Column(DateTime, nullable=True)
    ends_at: datetime = Column(DateTime, nullable=True)

    test_instance_id: int = Column(Integer, ForeignKey('test_instance.id'))
