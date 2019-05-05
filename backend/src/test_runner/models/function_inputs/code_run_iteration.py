from sqlalchemy import Integer, Column, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

from models import Base
from models.code_run_status import CodeRunStatus
from models.function_inputs.declarative_input_item import DeclarativeInputItem


class CodeRunIteration(Base):
    __tablename__ = "code_run_iteration"

    id: int = Column(Integer, primary_key=True)
    actual_output: str = Column(Text)
    status: CodeRunStatus = Column(Enum(CodeRunStatus),
                                   nullable=False,
                                   default=CodeRunStatus.Success)
    iteration_template: DeclarativeInputItem = relationship("DeclarativeInputItem",
                                                            back_populates='code_run_iterations')

    question_answer: "QuestionAnswer" = relationship("QuestionAnswer", back_populates='answer_iteration_results')

    iteration_template_id: int = Column(Integer, ForeignKey('declarative_input_item.id'))
    question_answer_id: int = Column(Integer, ForeignKey('question_answer.id'))
