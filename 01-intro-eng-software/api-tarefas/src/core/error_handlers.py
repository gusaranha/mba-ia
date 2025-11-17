from fastapi import Request
from fastapi.responses import JSONResponse
from src.core.exceptions import BaseAPIError


async def base_error_handler(request: Request, exc: BaseAPIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "details": exc.details
        }
    )
