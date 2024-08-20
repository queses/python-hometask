from datetime import datetime
from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, MappedAsDataclass
from sqlalchemy.sql import func

from src.models import BaseModel
from src.profile.profile_model import Profile


class ContractStatus(StrEnum):
    new = "new"
    in_progress = "in_progress"
    terminated = "terminated"


class Contract(MappedAsDataclass, BaseModel):
    __tablename__ = "contract"

    def __init__(self, terms: str, client: Profile, contractor: Profile):
        super().__init__()
        self.terms = terms
        self.status = ContractStatus.new
        self.client = client
        self.contractor = contractor

    id: Mapped[int] = mapped_column(primary_key=True)
    terms: Mapped[str]
    status: Mapped[ContractStatus]
    client_id: Mapped[int] = mapped_column(ForeignKey(Profile.id))
    client: Mapped[Profile] = relationship(foreign_keys=[client_id], compare=False)
    contractor_id: Mapped[int] = mapped_column(ForeignKey(Profile.id))
    contractor: Mapped[Profile] = relationship(foreign_keys=[contractor_id], compare=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
