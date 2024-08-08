from _datetime import datetime

from flask import Flask, json
from dotenv import load_dotenv

from hometask.exceptions import AppException
from hometask.orm import Orm
from hometask.routers import ContractsRouter

load_dotenv()

app = Flask(__name__)


# @app.teardown_appcontext
# def shutdown_session(exception=None) -> None:
# TODO
#     # https://docs.sqlalchemy.org/en/14/orm/contextual.html#using-thread-local-scope-with-web-applications
#     Orm().engine().remove()


class CustomJSONEncoder(json.provider.DefaultJSONProvider):
    @staticmethod
    def _custom_default(o):
        if isinstance(o, datetime):
            return o.isoformat()  # Convert datetime object to ISO 8601 format string
        return json.provider.DefaultJSONProvider.default(o)

    default = _custom_default


@app.errorhandler(AppException)
def handle_app_exception(e):
    return e.to_dict(), e.code


app.json = CustomJSONEncoder(app)
app.register_error_handler(AppException, handle_app_exception)

orm = Orm()
ContractsRouter(app, orm)
