from functools import wraps
from http import HTTPStatus

from flask import Flask, request

from src.exceptions import AppException
from src.services.contract_service import ContractService
from src.orm import Orm


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


def contracts(app: Flask):
    orm = Orm()

    @app.route("/contracts/<int:contract_id>", methods=["GET"])
    @authenticate()
    def contracts_get_one(contract_id: int, profile_id: int):
        return ContractService(orm.session()).get_by_id(contract_id, profile_id).to_dict()
