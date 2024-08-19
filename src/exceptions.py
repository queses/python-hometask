from http import HTTPStatus


class AppException(Exception):
    def __init__(self, code: HTTPStatus, message: str, data: object | None = None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):
        return {"code": self.code, "message": self.message, "data": self.data}

    pass
