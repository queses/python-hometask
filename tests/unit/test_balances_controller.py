from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.profile.balances_controller import DepositToBalanceData


class TestBalancesController:
    def test_deposit_validation(self):
        data: dict = {"amount": "1.0"}
        DepositToBalanceData(**data)

        data = {"amount": 1.554}
        assert DepositToBalanceData(**data).amount == Decimal("1.55")

        data = {"amount": 1.555}
        assert DepositToBalanceData(**data).amount == Decimal("1.56")

        with pytest.raises(ValidationError):
            data = {"amount": "abc"}
            DepositToBalanceData(**data)

        with pytest.raises(ValidationError):
            data = {"amount": "0.0"}
            DepositToBalanceData(**data)
