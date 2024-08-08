from http import HTTPStatus


class AppException(Exception):
    def __init__(self, code: HTTPStatus, message: str):
        self.code = code
        self.message = message

    def to_dict(self):
        return {"code": self.code, "message": self.message}

    pass
