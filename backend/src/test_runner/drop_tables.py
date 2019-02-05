import os

from db_config import ENGINE
from models import Base
from utils.helpers import load_modules

load_modules(os.path.join(os.path.dirname(__file__), "models"), "models")
Base.metadata.drop_all(ENGINE)
