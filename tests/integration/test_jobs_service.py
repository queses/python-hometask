import pytest

from src.exceptions import NotFoundException, BadRequestException
from src.job.jobs_service import JobsService
from src.util.orm import Orm
from tests.integration.data_fixtures import (
    ProfileFixture,
    ContractFixture,
    JobFixture,
    DataFixture,
)


class TestContractsService:
    def setup_method(self):
        self.session = Orm().session()
        self.sut = JobsService(self.session)

        self.client_1 = ProfileFixture.client()
        self.client_2 = ProfileFixture.client()
        self.contractor_1 = ProfileFixture.client()
        self.contractor_2 = ProfileFixture.client()
        self.contract_1 = ContractFixture(self.client_1, self.contractor_1)
        self.contract_2_terminated = ContractFixture(self.client_1, self.contractor_1).terminated()
        self.contract_3_other = ContractFixture(self.client_1, self.contractor_2)
        self.job_1 = JobFixture(self.contract_1)
        self.job_2_terminated = JobFixture(self.contract_2_terminated)
        self.job_3_paid = JobFixture(self.contract_1).paid()
        self.job_4_other = JobFixture(self.contract_3_other)

    def teardown_method(self):
        self.session.rollback()
        self.session.close()

    def test_get_unpaid(self):
        DataFixture.save_flush(
            self.session,
            self.job_1,
            self.job_2_terminated,
            self.job_3_paid,
            self.job_4_other,
        )

        res_client = self.sut.list_unpaid(self.client_1.m.id)
        assert len(res_client) == 2
        assert self.job_1.m in res_client
        assert self.job_4_other.m in res_client

        res_contractor_1 = self.sut.list_unpaid(self.contractor_1.m.id)
        assert len(res_contractor_1) == 1
        assert self.job_1.m in res_contractor_1

        res_contractor_2 = self.sut.list_unpaid(self.contractor_2.m.id)
        assert len(res_contractor_2) == 1
        assert self.job_4_other.m in res_contractor_2

    def test_get_unpaid_unauthorized(self):
        DataFixture.save_flush(self.session, self.contractor_2, self.job_1)

        res = self.sut.list_unpaid(self.contractor_2.m.id)
        assert len(res) == 0

    def test_pay(self):
        DataFixture.save_flush(
            self.session,
            self.job_1,
            self.job_4_other,
        )
        client_old_balance = self.client_1.m.balance
        contractor_old_balance = self.contractor_1.m.balance

        self.sut.pay(self.job_1.m.id, self.client_1.m.id)

        assert self.job_1.m.paid is True
        assert self.job_1.m.payment_date is not None

        assert self.client_1.m.balance == client_old_balance - self.job_1.m.price
        assert self.contractor_1.m.balance == contractor_old_balance + self.job_1.m.price

        assert self.job_4_other.m.paid is False

    def test_pay_unauthorized(self):
        DataFixture.save_flush(
            self.session,
            self.client_2,
            self.job_1,
        )

        with pytest.raises(NotFoundException):
            self.sut.pay(self.job_1.m.id, self.client_2.m.id)

        with pytest.raises(NotFoundException):
            self.sut.pay(self.job_1.m.id, self.contractor_1.m.id)

    def test_pay_check_if_paid(self):
        DataFixture.save_flush(self.session, self.client_1, self.job_3_paid)

        with pytest.raises(NotFoundException):
            self.sut.pay(self.job_3_paid.m.id, self.client_1.m.id)

    def test_pay_check_if_enough_balance(self):
        job_price = 10
        DataFixture.save_flush(
            self.session,
            self.client_1.with_balance(job_price - 1),
            self.job_1.with_price(job_price),
        )

        with pytest.raises(BadRequestException):
            self.sut.pay(self.job_1.m.id, self.client_1.m.id)

    def test_get_unpaid_sum(self):
        DataFixture.save_flush(
            self.session,
            self.job_1,
            self.job_2_terminated,
            self.job_3_paid,
            self.job_4_other,
        )

        res = self.sut.get_unpaid_sum(self.client_1.m.id)
        assert res == self.job_1.m.price + self.job_2_terminated.m.price + self.job_4_other.m.price
