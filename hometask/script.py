import random

from dotenv import load_dotenv

from hometask.profile_service import ProfileService
from hometask.orm import Orm

random.seed()
load_dotenv()


def run() -> None:
    service = ProfileService(Orm().engine())
    service.delete_all()
    service.create()
    service.create()
    service.list_contractors()
    service.update_last_name()


if __name__ == "__main__":
    run()
