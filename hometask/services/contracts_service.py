from sqlalchemy import select, and_, Engine
from sqlalchemy.orm import Session

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
        with Session(self.db) as session:
            query = select(Profile).where(and_(Profile.type == ProfileType.contractor))
            print("Profiles:")
            for profile in session.execute(query).all():
                print(profile)

    def update_profile(self):
        with Session(self.db) as session:
            print("Updating profiles:")
            for profile in session.execute(select(Profile).order_by(Profile.id.desc())).first():
                print("Updating profile " + str(profile.id))
                profile.last_name = "Wick"
            session.commit()
