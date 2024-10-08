from os import getenv, environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


# Singleton
class Orm(object):
    __instance = None
    __engine = None

    def __new__(cls):
        if cls.__instance:
            return cls.__instance

        cls.__instance = super(Orm, cls).__new__(cls)
        return cls.__instance

    def engine(self):
        if self.__engine:
            return self.__engine

        db_url = getenv("DB_URL")
        if "PYTEST_CURRENT_TEST" in environ:
            db_url = getenv("TEST_DB_URL")

        db_echo = getenv("DB_ECHO")
        self.__engine = create_engine(
            db_url if db_url else "", echo=True if db_echo == "1" else False
        )

        return self.__engine

    def sessionmaker(self):
        return sessionmaker(self.engine())

    def session(self):
        return Session(self.engine())
