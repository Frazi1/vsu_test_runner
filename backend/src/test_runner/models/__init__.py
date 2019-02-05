import os

from sqlalchemy.ext.declarative import declarative_base

from utils.helpers import load_modules

Base = declarative_base()


models = os.path.join(os.path.dirname(__file__))
load_modules(models, "models")
