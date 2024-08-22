from flask import request, Flask
from pydantic import BaseModel
from sqlalchemy.orm import scoped_session, Session

from src.exceptions import ForbiddenException
from src.profile.balances_service import BalancesService
from src.util.datatypes import PositiveMoney


class DepositToBalanceData(BaseModel):
    amount: PositiveMoney


class BalancesController:
    def __init__(self, app: Flask, get_session: scoped_session[Session]):
        self.app = app
        self.get_session = get_session

    def register(self):
        self.app.route("/balances/<int:user_id>/deposit", methods=["POST"])(self.deposit)

    def service(self):
        return BalancesService(self.get_session())

    def deposit(self, profile_id: int, user_id: int):
        data = DepositToBalanceData(**request.get_json())
        if profile_id != user_id:
            raise ForbiddenException("You can deposit to your own balances")
        return self.service().deposit(user_id, data.amount).to_dict()
