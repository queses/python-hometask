import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

from hometask.services.contracts_service import ContractsService

load_dotenv()

db = create_engine(os.getenv("DB_URL"), echo=True)


def run() -> None:
    service = ContractsService(db)
    # service.create_profile()
    service.get_contractors()
    service.update_profile()


if __name__ == "__main__":
    run()
