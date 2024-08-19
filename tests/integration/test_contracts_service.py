import pytest

from src.contracts.contracts_service import ContractsService
from src.exceptions import AppException
from src.util.orm import Orm
from tests.integration.data_fixtures import ProfileFixture, ContractFixture, DataFixture


class TestContractsService:
    def setup_class(self):
        self.session = Orm().session()
        self.sut = ContractsService(self.session)

        self.client_1 = ProfileFixture.client()
        self.client_2 = ProfileFixture.client()
        self.contractor_1 = ProfileFixture.contractor()
        self.contractor_2 = ProfileFixture.contractor()
        self.contract_1 = ContractFixture(self.client_1, self.contractor_1)
        self.contract_2_in_progress = ContractFixture(
            self.client_1, self.contractor_1
        ).in_progress()
        self.contract_3_terminated = ContractFixture(self.client_1, self.contractor_1).terminated()

    def test_get_by_id(self):
        DataFixture.save_flush(self.session, self.contract_1)

        res_client = self.sut.get_by_id(self.contract_1.m.id, self.client_1.m.id)
        assert res_client == self.contract_1.m

        res_contractor = self.sut.get_by_id(self.contract_1.m.id, self.contractor_1.m.id)
        assert res_contractor == self.contract_1.m

    def test_get_by_id_unauthorized(self):
        DataFixture.save_flush(
            self.session,
            self.contract_1,
            self.client_2,
            self.contractor_2,
        )
        self.session.flush()

        with pytest.raises(AppException) as e:
            self.sut.get_by_id(self.contract_1.m.id, self.client_2.m.id)
        assert e.value.code == 404

        with pytest.raises(AppException) as e:
            self.sut.get_by_id(self.contract_1.m.id, self.client_2.m.id)
        assert e.value.code == 404

        with pytest.raises(AppException) as e:
            self.sut.get_by_id(self.contract_1.m.id, self.contractor_2.m.id)
        assert e.value.code == 404

    def test_list_active(self):
        DataFixture.save_flush(
            self.session,
            self.contract_1,
            self.contract_2_in_progress,
            self.contract_3_terminated,
        )

        res = self.sut.list_active(self.client_1.m.id)

        assert len(res) == 2
        assert self.contract_1.m in res
        assert self.contract_2_in_progress.m in res

    def test_list_active_unauthorized(self):
        DataFixture.save_flush(
            self.session,
            self.contract_1,
            self.client_2,
            self.contractor_2,
        )

        res_client = self.sut.list_active(self.client_2.m.id)
        assert len(res_client) == 0

        res_contractor = self.sut.list_active(self.contractor_2.m.id)
        assert len(res_contractor) == 0
