from datetime import datetime, UTC
from decimal import Decimal
from typing import TypeVar, Generic

from faker import Faker
from sqlalchemy.orm import Session

from src.enums import ProfileType, ContractStatus
from src.models import Profile, Contract, Job

fake = Faker()

T = TypeVar("T")
M = TypeVar("M")


class DataFixture(Generic[T]):
    _model: T
    __deps: set["DataFixture"] | None = None
    __added = False

    @staticmethod
    def save(session: Session, *data_fixtures: "DataFixture"):
        for data_fixture in data_fixtures:
            data_fixture.add(session)

    @staticmethod
    def save_flush(session: Session, *data_fixtures: "DataFixture"):
        DataFixture.save(session, *data_fixtures)
        session.flush()

    @property
    def m(self) -> T:
        if not self.__added:
            raise Exception(f"Cannot access the data fixture model that is not added to the session: {type(self).__name__!r}")
        return self._model

    def add(self, session: Session):
        if self.__added:
            return self._model

        for dep in self.__deps or set():
            dep.add(session)

        session.add(self._model)
        self.__added = True

        return self._model

    def _unwrap(self, data_fixture: "DataFixture[M]") -> M:
        if self.__deps is None:
            self.__deps = set()
        self.__deps.add(data_fixture)

        return data_fixture._model


class ProfileFixture(DataFixture[Profile]):
    @staticmethod
    def client():
        return ProfileFixture(ProfileType.client)

    @staticmethod
    def contractor():
        return ProfileFixture(ProfileType.contractor)

    def __init__(self, profile_type: ProfileType):
        self._model = Profile(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            profession=fake.job(),
            profile_type=profile_type,
        )
        self._model.balance = Decimal(100)

    def with_balance(self, value: Decimal | int):
        self._model.balance = value if isinstance(value, Decimal) else Decimal(value)
        return self


class ContractFixture(DataFixture[Contract]):
    def __init__(self, client: ProfileFixture, contractor: ProfileFixture):
        self._model = Contract(
            terms=fake.text(10),
            client=self._unwrap(client),
            contractor=self._unwrap(contractor),
        )

    def in_progress(self):
        self._model.status = ContractStatus.in_progress
        return self

    def terminated(self):
        self._model.status = ContractStatus.terminated
        return self


class JobFixture(DataFixture[Job]):
    def __init__(self, contract: ContractFixture):
        self._model = Job(
            description=fake.text(10),
            price=Decimal(10),
            contract=self._unwrap(contract),
        )

    def with_price(self, value: Decimal | int):
        self._model.price = value if isinstance(value, Decimal) else Decimal(value)
        return self

    def paid(self):
        self._model.paid = True
        self._model.payment_date = datetime.now(UTC)
        return self
