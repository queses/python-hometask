from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, relationship
from sqlalchemy.sql import func

from src.contract.contract_model import Contract
from src.models import BaseModel


class Job(MappedAsDataclass, BaseModel):
    __tablename__ = "job"

    def __init__(self, description: str, price: Decimal, contract: Contract):
        super().__init__()
        self.description = description
        self.price = price
        self.contract = contract

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    price: Mapped[Decimal]
    contract_id: Mapped[int] = mapped_column(ForeignKey(Contract.id))
    contract: Mapped[Contract] = relationship(foreign_keys=[contract_id])
    payment_date: Mapped[Optional[datetime]]
    paid: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
