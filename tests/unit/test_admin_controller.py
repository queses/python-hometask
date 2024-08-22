from datetime import datetime

import pytest
from pydantic import ValidationError

from src.admin.admin_controller import GetBestProfessionData


class TestAdminController:
    def test_get_best_profession_validation(self):
        data: dict = {"start": "2024-01-01 00:00:00", "end": "2024-01-02"}
        GetBestProfessionData(**data)
        assert GetBestProfessionData(**data).end == datetime.fromisoformat("2024-01-02 00:00:00")

        with pytest.raises(ValidationError):
            data = {"start": "2024-01-01 00:00:00", "end": "twenty twenty four"}
            GetBestProfessionData(**data)

        with pytest.raises(ValidationError):
            data = {"start": "2024-01-01 00:00:00", "end": -1}
            GetBestProfessionData(**data)
