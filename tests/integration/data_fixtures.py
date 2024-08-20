from datetime import datetime, UTC
from decimal import Decimal

from faker import Faker

from src.contract.contract_model import Contract, ContractStatus
from src.job.job_model import Job
from src.profile.profile_model import Profile, ProfileType
from tests.integration.util.data_fixture import DataFixture

fake = Faker()


class ProfileFixture(DataFixture[Profile]):
    @staticmethod
    def client():
        return ProfileFixture(ProfileType.client)

    @staticmethod
    def contractor():
        return ProfileFixture(ProfileType.contractor)

    def __init__(self, profile_type: ProfileType):
        self._m = Profile(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            profession=fake.job(),
            profile_type=profile_type,
        )
        self._m.balance = Decimal(100)

    def with_balance(self, value: Decimal | int):
        self._m.balance = value if isinstance(value, Decimal) else Decimal(value)
        return self


class ContractFixture(DataFixture[Contract]):
    def __init__(self, client: ProfileFixture, contractor: ProfileFixture):
        self._m = Contract(
            terms=fake.text(10),
            client=self._unwrap(client),
            contractor=self._unwrap(contractor),
        )

    def in_progress(self):
        self._m.status = ContractStatus.in_progress
        return self

    def terminated(self):
        self._m.status = ContractStatus.terminated
        return self


class JobFixture(DataFixture[Job]):
    def __init__(self, contract: ContractFixture):
        self._m = Job(
            description=fake.text(10),
            price=Decimal(10),
            contract=self._unwrap(contract),
        )

    def with_price(self, value: Decimal | int):
        self._m.price = value if isinstance(value, Decimal) else Decimal(value)
        return self

    def paid(self):
        self._m.paid = True
        self._m.payment_date = datetime.now(UTC)
        return self
