from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from hometask.enums.enums import ProfileType


class Base(DeclarativeBase):
    pass

class Profile(Base):
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
    balance: Mapped[Decimal] = mapped_column(default=0)
    type: Mapped[ProfileType]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"#{self.id!r} {self.first_name} {self.last_name} (created {self.created_at.isoformat()!r}, updated {self.updated_at.isoformat()!r})"
