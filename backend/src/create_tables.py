from src.db_config import engine
from src.models import Base

Base.metadata.create_all(engine)
