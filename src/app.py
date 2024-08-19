from http import HTTPStatus

from dotenv import load_dotenv
from flask import Flask
from pydantic import ValidationError
from sqlalchemy.orm import scoped_session

from src.contracts.contracts_controller import ContractsController
from src.exceptions import AppException
from src.jobs.jobs_controller import JobsController
from src.util.orm import Orm
from src.util.flask import CustomJSONEncoder

load_dotenv()

app = Flask(__name__)
app.json = CustomJSONEncoder(app)

orm = Orm()
Session = scoped_session(Orm().sessionmaker())


@app.errorhandler(AppException)
def handle_app_exception(e: AppException):
    Session().rollback()
    return e.to_dict(), e.code


@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    app_e = AppException(HTTPStatus.BAD_REQUEST, "Validation error", e.errors())
    return handle_app_exception(app_e)


@app.teardown_appcontext
def shutdown_session(exception=None) -> None:
    if not exception:
        Session.commit()
    else:
        Session.rollback()
    Session.remove()


ContractsController(app=app, get_session=Session).register()
JobsController(app=app, get_session=Session).register()
