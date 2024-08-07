import random

from sqlalchemy import select, Engine
from sqlalchemy.orm import Session

from hometask.enums import ProfileType
from hometask.models import Profile


class ProfileService:
    def __init__(self, db: Engine):
        self.db = db

    def create(self):
        with Session(self.db) as session:
            profile = Profile(
                first_name="John",
                last_name="Doe",
                profession="Killer",
                profile_type=ProfileType.contractor,
            )

            print("Creating profile")
            session.add(profile)
            session.commit()
            print(profile)

    def list_contractors(self):
        with Session(self.db) as session:
            query = select(Profile).where(Profile.type == ProfileType.contractor)
            print("Profiles:")
            for profile in session.scalars(query).all():
                print(profile)

    def update_last_name(self):
        with Session(self.db) as session:
            query = select(Profile).order_by(Profile.id.desc())

            profile = session.scalars(query).first()
            if not profile:
                return

            last_name = f"Wick {random.randint(1, 100)!r}"
            print(f"Updating profile {profile.id} last name to {last_name!r}")
            profile.last_name = last_name

            session.commit()
            print(profile)

    def delete_all(self):
        with Session(self.db) as session:
            session.query(Profile).delete()
            session.commit()
