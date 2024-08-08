from http import HTTPStatus

from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import or_

from hometask.enums import ContractStatus
from hometask.exceptions import AppException
from hometask.models import Contract


class ContractService:
    def __init__(self, orm_sessionmaker: sessionmaker[Session]):
        self.orm_sessionmaker = orm_sessionmaker

    def get_by_id(self, contract_id: int, profile_id: int) -> Contract:
        with self.orm_sessionmaker() as session:
            contract = (
                session.query(Contract)
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
        with self.orm_sessionmaker() as session:
            contracts = (
                session.query(Contract)
                .filter(
                    or_(Contract.client_id == profile_id, Contract.contractor_id == profile_id),
                    Contract.status != ContractStatus.terminated,
                )
                .all()
            )
            return contracts
