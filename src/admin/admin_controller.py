from datetime import datetime

from flask import Flask, request
from pydantic import BaseModel, Field
from sqlalchemy.orm import scoped_session, Session

from src.admin.admin_service import AdminService

class GetBestProfessionData(BaseModel):
    start: datetime = Field(gt=0)
    end: datetime = Field(gt=0)

class GetBestClientsData(BaseModel):
    start: datetime
    end: datetime
    limit: int = Field(default=2, gt=0, lt=100)

class AdminController:
    def __init__(self, app: Flask, get_session: scoped_session[Session]):
        self.app = app
        self.get_session = get_session

    def register(self):
        self.app.route("/admin/best-profession", methods=["POST"])(self.get_best_profession)
        self.app.route("/admin/best-clients", methods=["POST"])(self.get_best_clients)

    def service(self):
        return AdminService(self.get_session())

    def get_best_profession(self):
        data = GetBestProfessionData(**request.get_json())
        return self.service().best_profession(start=data.start, end=data.end)

    def get_best_clients(self):
        data = GetBestClientsData(**request.get_json())
        return self.service().best_clients(start=data.start, end=data.end, limit=data.limit)
