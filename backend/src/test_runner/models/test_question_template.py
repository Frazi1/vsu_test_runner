from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey, Text, BigInteger, text, Boolean
from sqlalchemy.orm import relationship

from . import Base

if TYPE_CHECKING:
    from models.code_snippet import CodeSnippet


class TestQuestionTemplate(Base):
    __tablename__ = "test_question_template"

    def __init__(self, id_, name, description, time_limit, solution_code_snippet, version, is_deleted, *args, **kwargs):
        self.id = id_
        self.name = name
        self.description = description
        self.time_limit = time_limit
        self.solution_code_snippet = solution_code_snippet
        self.version = version
        self.is_deleted = is_deleted
        super(TestQuestionTemplate, self).__init__(*args, **kwargs)

    id: int = Column(Integer, primary_key=True)
    name: name = Column(String(100), nullable=False, default="")
    description: str = Column(Text, nullable=True)
    time_limit: int = Column(Integer, nullable=True)
    solution_code_snippet: CodeSnippet = relationship("CodeSnippet", back_populates="question_template")
    version: int = Column(BigInteger, server_default=text('1'))  # TODO: increment version on update
    is_deleted: bool = Column(Boolean, server_default=text('FALSE'))

    solution_code_snippet_id = Column(Integer, ForeignKey("code_snippet.id"), nullable=True)


def __repr__(self):
    return "<TestQuestionTemplate(id='{}', name='{}', description='{}', time_limit='{}'".format(self.id,
                                                                                                self.name,
                                                                                                self.description,
                                                                                                self.time_limit)
