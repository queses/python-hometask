from src.enums import ProfileType, ContractStatus
from src.models import Profile, Contract


class ProfileDataFixture:
    @staticmethod
    def client(last_name="One"):
        return Profile(
            first_name="Client",
            last_name=last_name,
            profession="Test client",
            profile_type=ProfileType.client,
        )

    @staticmethod
    def contractor(last_name="One"):
        return Profile(
            first_name="Contractor",
            last_name=last_name,
            profession="Test contractor",
            profile_type=ProfileType.contractor,
        )


class ContractDataFixture:
    @staticmethod
    def new(client: Profile, contractor: Profile):
        return Contract(
            terms="Test contract",
            client=client,
            contractor=contractor,
        )

    @staticmethod
    def in_progress(*args, **kwargs):
        contract = ContractDataFixture.new(*args, **kwargs)
        contract.status = ContractStatus.in_progress
        return contract

    @staticmethod
    def terminated(*args, **kwargs):
        contract = ContractDataFixture.new(*args, **kwargs)
        contract.status = ContractStatus.terminated
        return contract
