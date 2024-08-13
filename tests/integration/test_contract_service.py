from src.enums import ProfileType, ContractStatus
from src.exceptions import AppException
from src.models import Profile, Contract
from src.orm import Orm
from src.services.contract_service import ContractService


class TestContractService:
    def setup_class(self):
        self.session = Orm().session()
        self.service = ContractService(self.session)

        self.client_1 = Profile(
            first_name="Client",
            last_name="One",
            profession="Test client",
            profile_type=ProfileType.client,
        )
        self.client_2 = Profile(
            first_name="Client",
            last_name="Two",
            profession="Test client",
            profile_type=ProfileType.client,
        )
        self.contractor_1 = Profile(
            first_name="Contractor",
            last_name="One",
            profession="Test contractor",
            profile_type=ProfileType.contractor,
        )
        self.contractor_2 = Profile(
            first_name="Contractor",
            last_name="Two",
            profession="Test contractor",
            profile_type=ProfileType.contractor,
        )
        self.contract_1 = Contract(
            terms="Test contract",
            client=self.client_1,
            contractor=self.contractor_1,
        )
        self.contract_2_in_progress = Contract(
            terms="Test contract",
            client=self.client_1,
            contractor=self.contractor_1,
        )
        self.contract_2_in_progress.status = ContractStatus.in_progress
        self.contract_3_terminated = Contract(
            terms="Test contract",
            client=self.client_1,
            contractor=self.contractor_1,
        )
        self.contract_3_terminated.status = ContractStatus.terminated

    def test_get_by_id(self):
        self.session.add_all([self.client_1, self.contractor_1, self.contract_1])
        self.session.flush()

        res_client = self.service.get_by_id(self.contract_1.id, self.client_1.id)
        assert res_client == self.contract_1

        res_contractor = self.service.get_by_id(self.contract_1.id, self.contractor_1.id)
        assert res_contractor == self.contract_1

    def test_get_by_id_unauthorized(self):
        self.session.add_all([self.client_1, self.contractor_1, self.contract_1, self.client_2])
        self.session.flush()

        try:
            self.service.get_by_id(self.contract_1.id, self.client_2.id)
        except AppException as e:
            assert e.code == 404
        try:
            self.service.get_by_id(self.contract_1.id, self.contractor_2.id)
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

        res = self.service.list_active(self.client_1.id)
        assert len(res) == 2
        assert self.contract_1 in res
        assert self.contract_2_in_progress in res

    def test_list_active_unauthorized(self):
        self.session.add_all(
            [self.client_1, self.contractor_1, self.contract_1, self.client_2, self.contractor_2]
        )
        self.session.flush()

        res_client = self.service.list_active(self.client_2.id)
        assert len(res_client) == 0

        res_contractor = self.service.list_active(self.contractor_2.id)
        assert len(res_contractor) == 0
