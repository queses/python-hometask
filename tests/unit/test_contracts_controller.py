import pytest
from pydantic import ValidationError

from src.contract.contracts_controller import CreateContractData


class TestContractsController:
    def test_create_contract_validation(self):
        data: dict = {"contractor_id": 1, "terms": "ok"}
        CreateContractData(**data)

        with pytest.raises(ValidationError):
            data = {"contractor_id": "abc", "terms": "ok"}
            CreateContractData(**data)

        with pytest.raises(ValidationError):
            data = {"contractor_id": 1, "terms": 123}
            CreateContractData(**data)

        with pytest.raises(ValidationError):
            data = {"contractor_id": 1, "terms": ""}
            CreateContractData(**data)
