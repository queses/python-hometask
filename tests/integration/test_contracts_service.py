from src.contracts.contracts_service import ContractsService
from src.exceptions import AppException
from src.orm import Orm
from tests.integration.data_fixtures import ProfileDataFixture, ContractDataFixture


class TestContractsService:
    def setup_class(self):
        self.session = Orm().session()
        self.sut = ContractsService(self.session)

        self.client_1 = ProfileDataFixture.client()
        self.client_2 = ProfileDataFixture.client(last_name="Two")
        self.contractor_1 = ProfileDataFixture.contractor()
        self.contractor_2 = ProfileDataFixture.contractor(last_name="Two")
        self.contract_1 = ContractDataFixture.new(self.client_1, self.contractor_1)
        self.contract_2_in_progress = ContractDataFixture.in_progress(
            self.client_1, self.contractor_1
        )
        self.contract_3_terminated = ContractDataFixture.terminated(
            self.client_1, self.contractor_1
        )

    def test_get_by_id(self):
        self.session.add_all([self.client_1, self.contractor_1, self.contract_1])
        self.session.flush()

        res_client = self.sut.get_by_id(self.contract_1.id, self.client_1.id)
        assert res_client == self.contract_1

        res_contractor = self.sut.get_by_id(self.contract_1.id, self.contractor_1.id)
        assert res_contractor == self.contract_1

    def test_get_by_id_unauthorized(self):
        self.session.add_all([self.client_1, self.contractor_1, self.contract_1, self.client_2])
        self.session.flush()

        try:
            self.sut.get_by_id(self.contract_1.id, self.client_2.id)
        except AppException as e:
            assert e.code == 404
        try:
            self.sut.get_by_id(self.contract_1.id, self.contractor_2.id)
        except AppException as e:
            assert e.code == 404

    def test_list_active(self):
        self.session.add_all(
            [
                self.client_1,
                self.contractor_1,
                self.contract_1,
                self.contract_2_in_progress,
                self.contract_3_terminated,
            ]
        )
        self.session.flush()

        res = self.sut.list_active(self.client_1.id)
        assert len(res) == 2
        assert self.contract_1 in res
        assert self.contract_2_in_progress in res

    def test_list_active_unauthorized(self):
        self.session.add_all(
            [self.client_1, self.contractor_1, self.contract_1, self.client_2, self.contractor_2]
        )
        self.session.flush()

        res_client = self.sut.list_active(self.client_2.id)
        assert len(res_client) == 0

        res_contractor = self.sut.list_active(self.contractor_2.id)
        assert len(res_contractor) == 0
