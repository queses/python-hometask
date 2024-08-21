from decimal import Decimal

import pytest

from src.exceptions import BadRequestException
from src.profile.balances_service import BalancesService
from src.util.orm import Orm
from tests.integration.data_fixtures import (
    JobFixture,
    DataFixture,
)


class TestContractsService:
    def setup_method(self):
        self.session = Orm().session()
        self.sut = BalancesService(self.session)
        self.job_price = Decimal(10)

        self.job_1 = JobFixture().with_price(self.job_price)
        self.contract_1 = self.job_1.contract
        self.client_1 = self.contract_1.client
        self.job_2 = JobFixture(self.contract_1).with_price(self.job_price)
        self.job_3_paid = JobFixture(self.contract_1).paid().with_price(self.job_price)

    def teardown_method(self):
        self.session.rollback()
        self.session.close()

    def test_deposit(self):
        DataFixture.save_flush(self.session, self.job_1, self.job_2, self.job_3_paid)

        old_balance = self.client_1.m.balance

        self.sut.deposit(self.client_1.m.id, Decimal(1))
        assert self.client_1.m.balance == old_balance + 1

    def test_deposit_max_amount(self):
        DataFixture.save_flush(self.session, self.job_1, self.job_2)

        old_balance = self.client_1.m.balance

        with pytest.raises(BadRequestException):
            self.sut.deposit(self.client_1.m.id, self.job_price)  # 50% of unpaid jobs sum
        assert self.client_1.m.balance == old_balance

    def test_deposit_amount_positive(self):
        DataFixture.save_flush(self.session, self.job_1)

        old_balance = self.client_1.m.balance

        with pytest.raises(BadRequestException):
            self.sut.deposit(self.client_1.m.id, Decimal(0))
        with pytest.raises(BadRequestException):
            self.sut.deposit(self.client_1.m.id, Decimal(-1))

        assert self.client_1.m.balance == old_balance
