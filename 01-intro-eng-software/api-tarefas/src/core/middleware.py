from starlette.middleware.base import BaseHTTPMiddleware
from src.core.logger import log


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        log("INFO", "request_started", path=request.url.path, method=request.method)

        response = await call_next(request)

        log(
            "INFO",
            "request_finished",
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
        )

        return response
