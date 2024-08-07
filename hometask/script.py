import os
import random

from dotenv import load_dotenv
from sqlalchemy import create_engine

from hometask.services.profile_service import ProfileService

random.seed()
load_dotenv()

db_url = os.getenv("DB_URL")
db = create_engine(db_url if db_url else "", echo=True)


def run() -> None:
    service = ProfileService(db)
    service.delete_all()
    service.create()
    service.create()
    service.list_contractors()
    service.update_last_name()


if __name__ == "__main__":
    run()
