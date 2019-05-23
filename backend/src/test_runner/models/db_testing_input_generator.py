from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models import Base
from models.code_snippet import CodeSnippet


class DbTestingInputGenerator(Base):
    __tablename__ = "testing_input_generator"

    id: int = Column(Integer, primary_key=True)

    description: str = Column(String(255))
    code_snippet: CodeSnippet = relationship("CodeSnippet", back_populates="testing_input_generator")

    code_snippet_id: int = Column(Integer, ForeignKey('code_snippet.id'), nullable=False)

