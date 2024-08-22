from datetime import datetime
from decimal import Decimal
from typing import TypedDict

from sqlalchemy import func
from sqlalchemy.orm import Session

from src.contract.contract_model import Contract
from src.job.job_model import Job
from src.profile.profile_model import Profile


BestProfession = TypedDict("BestProfession", {"profession": str, "paid": Decimal})
BestClient = TypedDict("BestClient", {"id": int, "full_name": str, "paid": Decimal})


class AdminService:
    def __init__(self, session: Session):
        self.session = session

    def best_profession(self, start: datetime, end: datetime) -> BestProfession:
        query = (
            self.session.query(Profile.profession, func.sum(Job.price).label("paid"))
            .join(Job.contract)
            .join(Contract.contractor)
            .filter(
                Job.paid.is_(True),
                Job.created_at >= start, Job.created_at < end
            )
            .group_by(Profile.profession)
            .order_by(func.sum(Job.price).desc())
            .limit(1)
        )

        row = query.one()
        return {"profession": row.profession, "paid": row.paid}

    def best_clients(self, start: datetime, end: datetime, limit=2) -> list[BestClient]:
        query = (
            self.session.query(Profile.id, Profile.full_name, func.sum(Job.price).label("paid"))
            .join(Job.contract)
            .join(Contract.client)
            .filter(
                Job.paid.is_(True),
                Job.created_at >= start, Job.created_at < end
            )
            .group_by(Profile.id)
            .order_by(func.sum(Job.price).desc())
            .limit(limit)
        )

        rows = query.all()
        return [
            {"id": row.id, "full_name": row.full_name, "paid": row.paid}
            for row in rows
        ]
