from _datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from hometask.enums.enums import ProfileType


class Base(DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    profession: Mapped[str]
    balance: Mapped[Decimal] = mapped_column(default=0)
    type: Mapped[ProfileType]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, first_name={self.first_name!r})"
