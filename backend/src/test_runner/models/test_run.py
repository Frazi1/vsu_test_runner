from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from models import Base


class TestRun(Base):
    __tablename__ = "test_run"

    id = Column(Integer, primary_key=True)
    test_instance_id = Column(Integer, ForeignKey('test_instance.id'))
    test_instance = relationship("TestInstance", back_populates="test_runs")
    question_answers = relationship("QuestionAnswer", back_populates="test_run")
    started_at = Column(DateTime, server_default=func.now())
    finished_at = Column(DateTime, nullable=True)
    ends_at = Column(DateTime, nullable=True)