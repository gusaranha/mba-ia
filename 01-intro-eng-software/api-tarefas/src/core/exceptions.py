from typing import Any
from src.core.logger import log


class BaseAPIError(Exception):
    status_code = 500
    message = "Internal server error"

    def __init__(self, message: str | None = None, **details: Any):
        self.message = message or self.message
        self.details = details

        log(
            "ERROR",
            event=self.__class__.__name__,
            message=self.message,
            **details
        )

        super().__init__(self.message)


class BadRequestError(BaseAPIError):
    status_code = 400
    message = "Requisição inválida"


class NotFoundError(BaseAPIError):
    status_code = 404
    message = "Não encontrado"


class UnauthorizedError(BaseAPIError):
    status_code = 401
    message = "Não autorizado"
