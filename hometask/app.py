import os
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

db_url = os.getenv("DB_URL")
db = create_engine(db_url if db_url else "")

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"
