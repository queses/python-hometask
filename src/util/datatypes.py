from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator, Field


def _round_money(v: Decimal) -> Decimal:
    return round(v, 2)


Money = Annotated[Decimal, AfterValidator(_round_money)]

PositiveMoney = Annotated[Decimal, AfterValidator(_round_money), Field(gt=0)]
