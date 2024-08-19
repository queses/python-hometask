from datetime import datetime, UTC
from decimal import Decimal
from typing import TypeVar, Generic

from faker import Faker
from sqlalchemy.orm import Session, DeclarativeBase

from src.enums import ProfileType, ContractStatus
from src.models import Profile, Contract, Job

fake = Faker()

T = TypeVar("T")


class DataFixture(Generic[T]):
    model: T
    deps: list[DeclarativeBase] = []

    @staticmethod
    def save(session: Session, *data_fixtures: "DataFixture"):
        for data_fixture in data_fixtures:
            session.add(data_fixture.model)

    @staticmethod
    def save_flush(session: Session, *data_fixtures: "DataFixture"):
        DataFixture.save(session, *data_fixtures)
        session.flush()

    @property
    def m(self) -> T:
        return self.model

    def add(self, session: Session):
        for dep_model in self.deps:
            session.add(dep_model)
        session.add(self.model)

        return self.model


class ProfileDataFixture(DataFixture[Profile]):
    @staticmethod
    def client():
        return ProfileDataFixture(ProfileType.client)

    @staticmethod
    def contractor():
        return ProfileDataFixture(ProfileType.contractor)

    def __init__(self, profile_type: ProfileType):
        self.model = Profile(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            profession=fake.job(),
            profile_type=profile_type,
        )
        self.model.balance = Decimal(100)

    def with_balance(self, value: Decimal | int):
        self.model.balance = value if isinstance(value, Decimal) else Decimal(value)
        return self


class ContractDataFixture(DataFixture[Contract]):
    def __init__(self, client: Profile, contractor: Profile):
        self.deps = [client, contractor]
        self.model = Contract(
            terms=fake.text(),
            client=client,
            contractor=contractor,
        )

    def in_progress(self):
        self.model.status = ContractStatus.in_progress
        return self

    def terminated(self):
        self.model.status = ContractStatus.terminated
        return self


class JobDataFixture(DataFixture[Job]):
    def __init__(self, contract: Contract):
        self.deps = [contract]
        self.model = Job(
            description=fake.text(),
            price=Decimal(10),
            contract=contract,
        )

    def with_price(self, value: Decimal | int):
        self.model.price = value if isinstance(value, Decimal) else Decimal(value)
        return self

    def paid(self):
        self.model.paid = True
        self.model.payment_date = datetime.now(UTC)
        return self
