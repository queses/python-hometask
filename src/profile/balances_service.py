from decimal import Decimal

from sqlalchemy.orm import Session

from src.exceptions import BadRequestException
from src.job.jobs_service import JobsService
from src.profile.profile_model import Profile, ProfileType


class BalancesService:
    def __init__(self, session: Session):
        self.session = session
        self.jobs_service = JobsService(session)

    def deposit(self, client_id: int, amount: Decimal):
        if amount <= 0:
            raise BadRequestException("Amount must be positive")

        profile = (
            self.session.query(Profile)
            .filter(Profile.id == client_id, Profile.type == ProfileType.client)
            .with_for_update()
            .first()
        )
        if not profile:
            raise BadRequestException("Profile not found")

        unpaid_sum = self.jobs_service.get_unpaid_sum(client_id)
        if amount > unpaid_sum * Decimal(0.25):
            raise BadRequestException("Amount exceeds 25% of unpaid jobs sum")

        profile.balance += amount
        self.session.flush()

        return profile
