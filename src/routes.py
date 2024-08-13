from functools import wraps
from http import HTTPStatus

from flask import Flask, request
from sqlalchemy.orm import scoped_session, Session

from src.exceptions import AppException
from src.services.contract_service import ContractService


# Place this AFTER @app.route:
def authenticate():
    def _authenticate(func):
        @wraps(func)
        def authenticate_wrapper(*args, **kwargs):
            profile_id_header = request.headers.get("profile_id")
            try:
                profile_id = int(profile_id_header if profile_id_header else "")
            except ValueError:
                raise AppException(HTTPStatus.UNAUTHORIZED, "Invalid profile_id")

            kwargs["profile_id"] = profile_id
            return func(*args, **kwargs)

        return authenticate_wrapper

    return _authenticate


def contracts(app: Flask, get_session: scoped_session[Session]) -> None:
    def get_service():
        return ContractService(get_session())

    @app.route("/contracts/<int:contract_id>", methods=["GET"])
    @authenticate()
    def get_by_id(contract_id: int, profile_id: int):
        return get_service().get_by_id(contract_id, profile_id).to_dict()

    @app.route("/contracts", methods=["POST"])
    @authenticate()
    def create(profile_id: int):
        data = request.get_json()
        client_id = profile_id
        contractor_id = data.get("contractor_id")
        terms = data.get("terms")

        if not contractor_id or not terms:
            raise AppException(HTTPStatus.BAD_REQUEST, "contractor_id, and terms are required")

        return get_service().create(client_id, contractor_id, terms).to_dict()
