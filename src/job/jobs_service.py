from datetime import datetime, UTC
from decimal import Decimal

from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_, func

from src.contract.contract_model import Contract, ContractStatus
from src.exceptions import NotFoundException, BadRequestException
from src.job.job_model import Job
from src.profile.profile_model import Profile


class JobsService:
    def __init__(self, session: Session):
        self.session = session

    def list_unpaid(self, profile_id: int) -> list[Job]:
        jobs = (
            self.session.query(Job)
            .join(Job.contract)
            .filter(
                or_(Contract.client_id == profile_id, Contract.contractor_id == profile_id),
                Contract.status != ContractStatus.terminated,
                Job.paid.is_not(True),
            )
            .all()
        )

        return jobs

    def pay(self, job_id: int, client_id: int):
        query = (
            self.session.query(Job)
            .join(Job.contract)
            .join(aliased(Profile), Contract.client)
            .join(aliased(Profile), Contract.contractor)
            .filter(
                Job.id == job_id,
                Contract.client_id == client_id,
                Job.paid.is_not(True),
            )
        )

        job = query.with_for_update().first()
        if not job:
            raise NotFoundException("Job not found")

        if job.contract.client.balance < job.price:
            raise BadRequestException("Insufficient funds")

        job.paid = True
        job.payment_date = datetime.now(UTC)
        job.contract.client.balance -= job.price
        job.contract.contractor.balance += job.price

        self.session.flush()
        return job

    def get_unpaid_sum(self, client_id: int) -> Decimal:
        query = (
            self.session.query(func.sum(Job.price))
            .join(Job.contract)
            .filter(
                Contract.client_id == client_id,
                Job.paid.is_not(True),
            )
        )

        return query.scalar()
