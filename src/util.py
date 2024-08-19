from functools import wraps
from http import HTTPStatus

from flask import request

from src.exceptions import AppException


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
