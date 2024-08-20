import pytest
from pydantic import ValidationError

from src.contract.contracts_controller import CreateContract


class TestContractsController:
    def test_invalid_create_contract(self):
        with pytest.raises(ValidationError):
            data = {"contractor_id": "abc", "terms": "ok"}
            CreateContract(**data)
        with pytest.raises(ValidationError):
            data = {"contractor_id": 1, "terms": 123}
            CreateContract(**data)
        with pytest.raises(ValidationError):
            data = {"contractor_id": 1, "terms": ""}
            CreateContract(**data)
