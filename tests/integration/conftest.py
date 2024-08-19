import pytest
from dotenv import load_dotenv

from src.models import BaseModel
from src.util.orm import Orm


@pytest.fixture(scope="session", autouse=True)
def init():
    load_dotenv()
    BaseModel.metadata.create_all(Orm().engine())
