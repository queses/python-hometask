from _datetime import datetime

from flask import Flask, json
from dotenv import load_dotenv
from sqlalchemy.orm import scoped_session

from src.exceptions import AppException
from src.orm import Orm
import src.routes as routes

load_dotenv()

app = Flask(__name__)


class CustomJSONEncoder(json.provider.DefaultJSONProvider):
    @staticmethod
    def _custom_default(o):
        if isinstance(o, datetime):
            return o.isoformat()  # Convert datetime object to ISO 8601 format string
        return json.provider.DefaultJSONProvider.default(o)

    default = _custom_default


app.json = CustomJSONEncoder(app)

orm = Orm()
Session = scoped_session(Orm().sessionmaker())


@app.errorhandler(AppException)
def handle_app_exception(e):
    Session().rollback()
    return e.to_dict(), e.code


@app.teardown_appcontext
def shutdown_session(exception=None) -> None:
    if not exception:
        Session.commit()
    else:
        Session.rollback()
    Session.remove()


routes.contracts(app=app, get_session=Session)
