from typing import TypeVar, List, Callable

from sqlalchemy.orm import Session

from models import Base


class BaseRepository(object):
    T = TypeVar('T', bound=Base)

    def __init__(self, session_provider: Callable[..., Session]):
        self.session_provider = session_provider

    @property
    def session(self) -> Session:
        return self.session_provider()

    def get_by_id(self, id_: int) -> T:
        return self.session.query(self.T).filter(self.T.id == id_).first()

    def get_all(self) -> List[T]:
        return self.session.query(self.T).all()

    def add(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def commit(self):
        self.session.commit()
