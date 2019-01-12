import os

from src.db_config import ENGINE
from src.models import Base

from app import load_modules
load_modules(os.path.join(os.path.dirname(__file__), "models"), "src.models")
Base.metadata.create_all(ENGINE)
