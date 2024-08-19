from flask import Flask, request
from pydantic import BaseModel, Field
from sqlalchemy.orm import scoped_session, Session

from src.contracts.contracts_service import ContractsService
from src.util import authenticate


class CreateContract(BaseModel):
    contractor_id: int
    terms: str = Field(min_length=1)


class ContractsController:
    def __init__(self, app: Flask, get_session: scoped_session[Session]):
        self.app = app
        self.get_session = get_session

    def register(self):
        self.app.route("/contracts/<int:contract_id>", methods=["GET"])(self.get_by_id)
        self.app.route("/contracts", methods=["POST"])(self.create)

    def service(self):
        return ContractsService(self.get_session())

    @authenticate()
    def get_by_id(self, contract_id: int, profile_id: int):
        return self.service().get_by_id(contract_id, profile_id).to_dict()

    @authenticate()
    def create(self, profile_id: int):
        data = CreateContract(**request.get_json())

        return self.service().create(profile_id, data.contractor_id, data.terms).to_dict()
