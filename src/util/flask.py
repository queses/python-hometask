from datetime import datetime
from functools import wraps
from http import HTTPStatus

from flask import request, json

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


class CustomJSONEncoder(json.provider.DefaultJSONProvider):
    @staticmethod
    def _custom_default(o):
        if isinstance(o, datetime):
            return o.isoformat()  # Convert datetime object to ISO 8601 format string
        return json.provider.DefaultJSONProvider.default(o)

    default = _custom_default
