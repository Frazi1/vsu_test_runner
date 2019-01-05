from src.db_config import ENGINE
from src.models import Base

Base.metadata.create_all(ENGINE)
