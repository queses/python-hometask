from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass
from sqlalchemy.sql import func

from src.models import BaseModel


class ProfileType(StrEnum):
    client = "client"
    contractor = "contractor"


class Profile(MappedAsDataclass, BaseModel):
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

    @hybrid_property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name

    def __repr__(self) -> str:
        return f"#{self.id} {self.full_name} (created {self.created_at.isoformat()!r}, updated {self.updated_at.isoformat()!r})"
