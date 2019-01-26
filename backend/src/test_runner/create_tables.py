import os

from app import load_modules
from db_config import ENGINE
from models import Base

load_modules(os.path.join(os.path.dirname(__file__), "models"), "src.models")
Base.metadata.create_all(ENGINE)
