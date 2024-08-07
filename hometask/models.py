from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, MappedAsDataclass
from sqlalchemy.sql import func

from hometask.enums import ProfileType, ContractStatus


class Base(DeclarativeBase):
    pass
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class Profile(MappedAsDataclass, Base):
    __tablename__ = "profile"

    def __init__(self, first_name: str, last_name: str, profession: str, profile_type: ProfileType):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.profession = profession
        self.type = profile_type

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    profession: Mapped[str]
    type: Mapped[ProfileType]
    balance: Mapped[Decimal] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"#{self.id!r} {self.first_name} {self.last_name} (created {self.created_at.isoformat()!r}, updated {self.updated_at.isoformat()!r})"

class Contract(MappedAsDataclass, Base):
    __tablename__ = "contract"

    id: Mapped[int] = mapped_column(primary_key=True)
    terms: Mapped[str]
    status: Mapped[ContractStatus]
    client_id: Mapped[int] = mapped_column(ForeignKey(Profile.id))
    # client: Mapped[Profile] = relationship(foreign_keys=[client_id], compare=False)
    contractor_id: Mapped[int] = mapped_column(ForeignKey(Profile.id))
    # contractor: Mapped[Profile] = relationship(foreign_keys=[contractor_id], compare=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())


class Job(MappedAsDataclass, Base):
    __tablename__ = "job"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    price: Mapped[Decimal]
    contract_id: Mapped[int] = mapped_column(ForeignKey(Contract.id))
    contract: Mapped[Contract] = relationship(foreign_keys=[contract_id])
    payment_date: Mapped[Optional[datetime]]
    paid: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
