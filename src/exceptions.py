from http import HTTPStatus


class AppException(Exception):
    def __init__(self, code: HTTPStatus, message: str, data: object | None = None):
        self.code = code
        self.message = message
        self.data = data

    def to_dict(self):
        return {"code": self.code, "message": self.message, "data": self.data}


class NotFoundException(AppException):
    def __init__(self, message: str, data: object | None = None):
        super().__init__(HTTPStatus.NOT_FOUND, message, data)


class BadRequestException(AppException):
    def __init__(self, message: str, data: object | None = None):
        super().__init__(HTTPStatus.BAD_REQUEST, message, data)


class ForbiddenException(AppException):
    def __init__(self, message: str, data: object | None = None):
        super().__init__(HTTPStatus.FORBIDDEN, message, data)
