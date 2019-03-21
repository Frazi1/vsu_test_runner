from typing import List

from sqlalchemy import Column, String, Integer, DateTime, func, Boolean, text
from sqlalchemy.orm import relationship

from models import Base
from models.associations import test_instance_to_question_instance_association


class TestInstance(Base):
    __tablename__ = "test_instance"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    created_at = Column(DateTime, server_default=func.now())
    available_after = Column(DateTime, nullable=True)
    disabled_after = Column(DateTime, nullable=True)
    time_limit = Column(Integer, nullable=True)
    is_active = Column(Boolean, server_default=text('TRUE'))
    questions: List["QuestionInstance"] = relationship(
        "QuestionInstance",
        secondary=test_instance_to_question_instance_association,
        back_populates="tests"
    )

    test_runs = relationship("TestRun", back_populates="test_instance")
