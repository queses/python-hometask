import random

from dotenv import load_dotenv

from src.enums import ProfileType
from src.services.profile_service import ProfileService
from src.util.orm import Orm

random.seed()
load_dotenv()


def run() -> None:
    with Orm().session() as session:
        service = ProfileService(session)
        client_1 = service.create("John", "Smith", "Test client", ProfileType.client)
        print("Created", client_1)
        contractor_1 = service.create("John", "Miller", "Test contractor", ProfileType.contractor)
        print("Created", contractor_1)

        session.commit()


if __name__ == "__main__":
    run()
