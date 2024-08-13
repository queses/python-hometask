from http import HTTPStatus

from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.enums import ContractStatus
from src.exceptions import AppException
from src.models import Contract, Profile


class ContractService:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, contract_id: int, profile_id: int) -> Contract:
        contract = (
            self.session.query(Contract)
            .filter(
                Contract.id == contract_id,
                or_(Contract.client_id == profile_id, Contract.contractor_id == profile_id),
            )
            .first()
        )
        if not contract:
            raise AppException(HTTPStatus.NOT_FOUND, "Contract not found")

        return contract

    def list_active(self, profile_id: int):
        contracts = (
            self.session.query(Contract)
            .filter(
                or_(Contract.client_id == profile_id, Contract.contractor_id == profile_id),
                Contract.status != ContractStatus.terminated,
            )
            .all()
        )
        return contracts

    def create(self, client_id: int, contractor_id: int, terms: str) -> Contract:
        client = self.session.query(Profile).get(client_id)
        if not client:
            raise AppException(HTTPStatus.BAD_REQUEST, "Client not found")
        contractor = self.session.query(Profile).get(contractor_id)
        if not contractor:
            raise AppException(HTTPStatus.BAD_REQUEST, "Contractor not found")

        contract = Contract(terms=terms, client=client, contractor=contractor)
        self.session.add(contract)
        self.session.flush()

        return contract
