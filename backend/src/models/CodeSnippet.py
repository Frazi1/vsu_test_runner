from sqlalchemy.orm import relationship

from src.models import Base
from sqlalchemy import *

from src.models.LanguageEnum import LanguageEnum


class CodeSnippet(Base):
    __tablename__ = "code_snippet"

    id = Column(Integer, primary_key=True)
    language = Column(Enum(LanguageEnum))
    code = Column(Text)
    function_id = Column(Integer, ForeignKey('function.id'), nullable=false)
    function = relationship("Function", back_populates="code_snippets")

    def __init__(self, language, code, function_):
        if isinstance(code, list):
            code = "".join(x + "\n" for x in code)

        self.language = language
        self.code = code
        self.function = function_
