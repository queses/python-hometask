from _datetime import datetime

from dotenv import load_dotenv
from flask import Flask, json
from pydantic import ValidationError
from sqlalchemy.orm import scoped_session

from src.contracts.contracts_controller import ContractsController
from src.exceptions import AppException
from src.orm import Orm

load_dotenv()

app = Flask(__name__)

orm = Orm()
Session = scoped_session(Orm().sessionmaker())


class CustomJSONEncoder(json.provider.DefaultJSONProvider):
    @staticmethod
    def _custom_default(o):
        if isinstance(o, datetime):
            return o.isoformat()  # Convert datetime object to ISO 8601 format string
        return json.provider.DefaultJSONProvider.default(o)

    default = _custom_default


app.json = CustomJSONEncoder(app)


@app.errorhandler(AppException)
def handle_app_exception(e: AppException):
    Session().rollback()
    return e.to_dict(), e.code


@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    code = 400
    return {"code": code, "message": "Validation error", "data": e.errors()}, code


@app.teardown_appcontext
def shutdown_session(exception=None) -> None:
    if not exception:
        Session.commit()
    else:
        Session.rollback()
    Session.remove()


ContractsController(app=app, get_session=Session).register()
