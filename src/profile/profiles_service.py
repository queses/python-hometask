from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.exceptions import AppException
from src.profile.profile_model import Profile, ProfileType


class ProfileService:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self, first_name: str, last_name: str, profession: str, profile_type: ProfileType
    ) -> Profile:
        profile = Profile(
            first_name=first_name,
            last_name=last_name,
            profession=profession,
            profile_type=profile_type,
        )

        self.session.add(profile)
        self.session.flush()
        return profile

    def print_contractors(self):
        query = select(Profile).where(Profile.type == ProfileType.contractor)
        print("Profiles:")
        for profile in self.session.scalars(query).all():
            print(profile)

    def update_last_name(self, last_name: str) -> Profile:
        query = select(Profile).order_by(Profile.id.desc())

        profile = self.session.scalars(query).first()
        if not profile:
            raise AppException(HTTPStatus.NOT_FOUND, "Profile is not found")

        print(f"Updating profile {profile.id} last name to {last_name!r}")
        profile.last_name = last_name

        self.session.flush()
        return profile

    def delete_all(self, ids: list[int]):
        self.session.query(Profile).where(Profile.id.in_(ids)).delete()
        self.session.flush()
