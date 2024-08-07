from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import or_

from hometask.enums import ContractStatus
from hometask.exceptions import RequestException
from hometask.models import Contract


class ContractService:
    def __init__(self, make_session: sessionmaker[Session]):
        self.make_session = make_session

    def get_by_id(self, contract_id: int, profile_id: int):
        with self.make_session() as session:
            contract = (
                session.query(Contract)
                .filter(
                    Contract.id == contract_id,
                    or_(Contract.client_id == profile_id, Contract.contractor_id == profile_id),
                )
                .first()
            )
            if not contract:
                raise RequestException(404, "Contract not found")

            return contract

    def list_active(self, profile_id: int):
        with self.make_session() as session:
            contracts = (
                session.query(Contract)
                .filter(
                    or_(Contract.client_id == profile_id, Contract.contractor_id == profile_id),
                    Contract.status != ContractStatus.terminated,
                )
                .all()
            )
            return contracts
