import os
from src.infra.config.settings import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infra.db.settings.base import Base


class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = settings.DATABASE_URL
        self.__engine = self.__create_database_engine()
        Base.metadata.create_all(self.__engine)

    def __create_database_engine(self):
        engine = create_engine(
            self.__connection_string,
            connect_args={'check_same_thread': False}
        )
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()