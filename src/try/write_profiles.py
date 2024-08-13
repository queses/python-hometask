import random

from dotenv import load_dotenv

from src.services.profile_service import ProfileService
from src.orm import Orm

random.seed()
load_dotenv()


def run() -> None:
    with Orm().session() as session:
        service = ProfileService(session)
        contractor_1 = service.create_contractor("John", "Wick", "Killer")
        print("Created", contractor_1)
        contractor_2 = service.create_contractor("John", "Wick", "Killer")
        print("Created", contractor_2)

        service.print_contractors()
        new_last_name = f"Wick {random.randint(1, 100)!r}"
        updated = service.update_last_name(new_last_name)
        print("Updated", updated)
        service.print_contractors()

        service.delete_all([contractor_1.id, contractor_2.id])


if __name__ == "__main__":
    run()
