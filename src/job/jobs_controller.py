from flask import Flask
from sqlalchemy.orm import scoped_session, Session

from src.job.jobs_service import JobsService
from src.util.flask import authenticate


class JobsController:
    def __init__(self, app: Flask, get_session: scoped_session[Session]):
        self.app = app
        self.get_session = get_session

    def register(self):
        self.app.route("/jobs/unpaid", methods=["GET"])(self.list_unpaid)
        self.app.route("/jobs/pay/<int:job_id>", methods=["POST"])(self.pay)

    def service(self):
        return JobsService(self.get_session())

    @authenticate()
    def list_unpaid(self, profile_id: int):
        return [job.to_dict() for job in self.service().list_unpaid(profile_id)]

    @authenticate()
    def pay(self, job_id: int, profile_id: int):
        return self.service().pay(job_id, profile_id).to_dict()
