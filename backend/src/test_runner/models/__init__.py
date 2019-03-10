import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import ReprMixin

from utils.helpers import load_modules

Base = declarative_base()


class BaseModel(Base, ReprMixin):
    pass


models = os.path.join(os.path.dirname(__file__))
load_modules(models, "models")
