import json

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from hometask.orm import Orm
from hometask.services.contract_service import ContractService

load_dotenv()

orm_sessionmaker = Orm().sessionmaker()

app = Flask(__name__)


# def get_profile_decorator()
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             ctx.
#             result = func(*args, **kwargs)
#             return func
#         return wrapper


@app.route("/contracts/3", methods=["GET"])
def contracts_get_one():
    contract_id_str = "3"
    profile_id_str = request.headers.get("profile_id")
    try:
        contract_id = int(contract_id_str if contract_id_str else "")
    except ValueError:
        return "Contract ID is required", 400
    try:
        profile_id = int(profile_id_str if profile_id_str else "")
    except ValueError:
        return "Profile ID is required", 400

    resp = ContractService(orm_sessionmaker).get_by_id(contract_id, profile_id)
    return jsonify(resp)
