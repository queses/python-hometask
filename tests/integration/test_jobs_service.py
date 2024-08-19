import pytest

from src.exceptions import AppException
from src.jobs.jobs_service import JobsService
from src.orm import Orm
from tests.integration.data_fixtures import (
    ProfileDataFixture,
    ContractDataFixture,
    JobDataFixture,
    DataFixture,
)


class TestContractsService:
    def setup_method(self):
        self.session = Orm().session()
        self.sut = JobsService(self.session)

        self.client_1 = ProfileDataFixture.client()
        self.client_2 = ProfileDataFixture.client()
        self.contractor_1 = ProfileDataFixture.client()
        self.contractor_2 = ProfileDataFixture.client()
        self.contract_1 = ContractDataFixture(self.client_1.m, self.contractor_1.m)
        self.contract_2_terminated = ContractDataFixture(
            self.client_1.m, self.contractor_1.m
        ).terminated()
        self.contract_3_other = ContractDataFixture(self.client_1.m, self.contractor_2.m)
        self.job_1 = JobDataFixture(self.contract_1.m)
        self.job_2_terminated = JobDataFixture(self.contract_2_terminated.m)
        self.job_3_paid = JobDataFixture(self.contract_1.m).paid()
        self.job_4_other = JobDataFixture(self.contract_3_other.m)

    def teardown_method(self):
        self.session.rollback()
        self.session.close()

    def test_get_unpaid(self):
        DataFixture.save_flush(
            self.session,
            self.client_1,
            self.contractor_1,
            self.contractor_2,
            self.job_1,
            self.job_2_terminated,
            self.job_3_paid,
            self.job_4_other,
        )

        res_client = self.sut.get_unpaid(self.client_1.m.id)
        assert len(res_client) == 2
        assert self.job_1.m in res_client
        assert self.job_4_other.m in res_client

        res_contractor_1 = self.sut.get_unpaid(self.contractor_1.m.id)
        assert len(res_contractor_1) == 1
        assert self.job_1.m in res_contractor_1

        res_contractor_2 = self.sut.get_unpaid(self.contractor_2.m.id)
        assert len(res_contractor_2) == 1
        assert self.job_4_other.m in res_contractor_2

    def test_get_unpaid_unauthorized(self):
        DataFixture.save_flush(
            self.session,
            self.contractor_2,
            self.job_1,
        )

        res = self.sut.get_unpaid(self.contractor_2.m.id)
        assert len(res) == 0

    def test_pay(self):
        DataFixture.save_flush(
            self.session,
            self.client_1,
            self.contractor_1,
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
            self.contractor_1,
            self.job_1,
        )

        with pytest.raises(AppException) as e:
            self.sut.pay(self.job_1.m.id, self.client_2.m.id)
        assert e.value.code == 404

        with pytest.raises(AppException) as e:
            self.sut.pay(self.job_1.m.id, self.contractor_1.m.id)
        assert e.value.code == 404

    def test_pay_check_if_paid(self):
        DataFixture.save_flush(self.session, self.client_1, self.job_3_paid)

        with pytest.raises(AppException) as e:
            self.sut.pay(self.job_3_paid.m.id, self.client_1.m.id)
        assert e.value.code == 404

    def test_pay_check_if_enough_balance(self):
        job_price = 10
        DataFixture.save_flush(
            self.session,
            self.client_1.with_balance(job_price - 1),
            self.job_1.with_price(job_price),
        )

        with pytest.raises(AppException) as e:
            self.sut.pay(self.job_1.m.id, self.client_1.m.id)
        assert e.value.code == 400
