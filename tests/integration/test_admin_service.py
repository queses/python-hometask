from datetime import datetime, UTC, timedelta
from decimal import Decimal

from src.admin.admin_service import AdminService
from src.util.orm import Orm
from tests.integration.data_fixtures import JobFixture, ProfileFixture, ContractFixture
from tests.integration.util.data_fixture import DataFixture


class TestAdminService:
    def setup_method(self):
        self.session = Orm().session()
        self.sut = AdminService(self.session)

        self.job_price = Decimal(10)
        self.date_end = datetime.now(UTC) + timedelta(days=1)
        self.date_start = datetime.now(UTC) - timedelta(days=1)
        self.date_other = datetime.now(UTC) - timedelta(days=2)

        self.client_1 = ProfileFixture.client()
        self.contractor_1 = ProfileFixture.contractor()

        self.contract_1 = ContractFixture(self.client_1, self.contractor_1).in_progress()

        self.job_1 = JobFixture(self.contract_1).with_price(self.job_price).paid()
        self.job_2 = JobFixture(self.contract_1).with_price(self.job_price).paid()
        self.job_3_unpaid = JobFixture(self.contract_1).with_price(self.job_price)
        self.job_4_other_date = (
            JobFixture(self.contract_1)
            .with_price(self.job_price)
            .paid()
            .with_created_at(self.date_other)
        )

    def teardown_method(self):
        self.session.rollback()
        self.session.close()

    def test_best_clients(self):
        client_2 = ProfileFixture.client()
        client_3 = ProfileFixture.client()

        self.contract_2 = ContractFixture(client_2, self.contractor_1).in_progress()
        self.contract_3 = ContractFixture(client_3, self.contractor_1).in_progress()


        job_5 = JobFixture(self.contract_2).with_price(self.job_price).paid()
        job_6 = JobFixture(self.contract_3).with_price(self.job_price - 1).paid()

        DataFixture.save_flush(
            self.session, self.job_1, self.job_2, self.job_3_unpaid, self.job_4_other_date, job_5, job_6
        )

        result = self.sut.best_clients(start=self.date_start, end=self.date_end, limit=2)
        assert len(result) == 2
        assert result[0]["id"] == self.client_1.m.id
        assert result[0]["full_name"] == self.client_1.m.full_name
        assert result[0]["paid"] == self.job_price * 2
        assert result[1]["id"] == client_2.m.id
        assert result[1]["full_name"] == client_2.m.full_name
        assert result[1]["paid"] == self.job_price

    def test_best_profession(self):
        self.contractor_1 = self.contractor_1.with_profession("Profession A")
        contractor_2 = ProfileFixture.contractor().with_profession("Profession B")

        self.contract_2 = ContractFixture(self.client_1, contractor_2).in_progress()

        job_5 = JobFixture(self.contract_2).with_price(self.job_price).paid()

        DataFixture.save_flush(
            self.session, self.job_1, self.job_2, self.job_3_unpaid, self.job_4_other_date, job_5
        )

        result = self.sut.best_profession(start=self.date_start, end=self.date_end)
        assert result["profession"] == "Profession A"
        assert result["paid"] == self.job_price * 2
