from sqlalchemy import select, True_
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy import and_

from hometask.enums.enums import ProfileType
from hometask.models.models import Profile


class ContractsService:
    def __init__(self, db: Engine):
        self.db = db

    def create_profile(self):
        with Session(self.db) as session:
            profile = Profile(
                first_name="John",
                last_name="Doe",
                profession="Killer",
                type=ProfileType.contractor,
            )

            session.add(profile)
            session.commit()

    def get_contractors(self):
        session = Session(self.db)
        cond = and_(Profile.type == ProfileType.contractor)
        print("Profiles:")
        for profile in session.execute(select(Profile).where(cond)).all():
            print(profile)
