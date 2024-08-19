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
        contractor_1 = service.create("John", "Wick", "Killer", ProfileType.contractor)
        print("Created", contractor_1)
        contractor_2 = service.create("John", "Wick", "Killer", ProfileType.contractor)
        print("Created", contractor_2)

        service.print_contractors()
        new_last_name = f"Wick {random.randint(1, 100)!r}"
        updated = service.update_last_name(new_last_name)
        print("Updated", updated)
        service.print_contractors()


if __name__ == "__main__":
    run()
