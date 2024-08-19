from datetime import datetime, UTC
from http import HTTPStatus

from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_

from src.enums import ContractStatus
from src.exceptions import AppException
from src.models import Job, Contract, Profile


class JobsService:
    def __init__(self, session: Session):
        self.session = session

    def get_unpaid(self, profile_id: int) -> list[Job]:
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
        job = (
            self.session.query(Job)
            .join(Job.contract)
            .join(aliased(Profile), Contract.client)
            .join(aliased(Profile), Contract.contractor)
            .filter(
                Job.id == job_id,
                Contract.client_id == client_id,
                Contract.status != ContractStatus.terminated,
                Job.paid.is_not(True),
            )
            .with_for_update()
            .first()
        )
        if not job:
            raise AppException(HTTPStatus.NOT_FOUND, "Job not found")

        if job.contract.client.balance < job.price:
            raise AppException(HTTPStatus.BAD_REQUEST, "Insufficient funds")

        job.paid = True
        job.payment_date = datetime.now(UTC)
        job.contract.client.balance -= job.price
        job.contract.contractor.balance += job.price

        self.session.flush()
        return job
