import os
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import create_engine

from hometask.services.contracts_service import ContractsService

load_dotenv()

db = create_engine(os.getenv("DB_URL"))

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"
