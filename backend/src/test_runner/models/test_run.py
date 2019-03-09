from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from typing import List

from models import Base
from models.test_instance import TestInstance


class TestRun(Base):
    __tablename__ = "test_run"

    id = Column(Integer, primary_key=True)  # type: int
    test_instance = relationship("TestInstance", back_populates="test_runs")  # type: TestInstance
    question_answers = relationship("QuestionAnswer", back_populates="test_run")  # type: List["QuestionAnswer"]
    started_at = Column(DateTime, server_default=func.now())  # type: datetime
    finished_at = Column(DateTime, nullable=True)  # type: datetime
    ends_at = Column(DateTime, nullable=True)  # type: datetime

    test_instance_id = Column(Integer, ForeignKey('test_instance.id'))  # type: int
