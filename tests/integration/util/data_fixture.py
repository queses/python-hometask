from typing import Generic, TypeVar

from sqlalchemy.orm import Session

T = TypeVar("T")
M = TypeVar("M")


# abstract class for data fixtures
class DataFixture(Generic[T]):
    _m: T
    __deps: set["DataFixture"] | None = None
    __added = False

    # saves the data fixtures to the session
    @staticmethod
    def save(session: Session, *data_fixtures: "DataFixture"):
        for data_fixture in data_fixtures:
            data_fixture.add(session)

    # saves the data fixtures to the session and flushes the session
    @staticmethod
    def save_flush(session: Session, *data_fixtures: "DataFixture"):
        DataFixture.save(session, *data_fixtures)
        session.flush()

    # get the model; throws an exception if the model is not added to the session
    @property
    def m(self) -> T:
        if not self.__added:
            raise Exception(
                f"Cannot access the data fixture model that is not added to the session: {type(self).__name__!r}"
            )
        return self._m

    # adds the model and dependencies' models to the session
    def add(self, session: Session):
        if self.__added:
            return self._m

        for dep in self.__deps or set():
            dep.add(session)

        session.add(self._m)
        self.__added = True

        return self._m

    # gets the model from a related data fixture and adds it to the dependencies
    def _unwrap(self, data_fixture: "DataFixture[M]") -> M:
        if self.__deps is None:
            self.__deps = set()
        self.__deps.add(data_fixture)

        return data_fixture._m
