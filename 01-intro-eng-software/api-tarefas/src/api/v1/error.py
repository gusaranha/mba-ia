from fastapi import APIRouter
from src.core.exceptions import BadRequestError, NotFoundError, UnauthorizedError

router = APIRouter()

@router.get("/bad-request")
def bad_request():
    raise BadRequestError()


@router.get("/not-found")
def not_found():
    raise NotFoundError()

@router.get("/not-authorized")
def not_found():
    raise UnauthorizedError()
