import os

from helpers import load_modules
from db_config import ENGINE
from models import Base

load_modules(os.path.join(os.path.dirname(__file__), "models"), "models")
Base.metadata.drop_all(ENGINE)
