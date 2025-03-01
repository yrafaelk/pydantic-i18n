from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from pydantic_i18n import PydanticI18n, JsonLoader

__all__ = ["get_locale", "validation_exception_handler"]


DEFAULT_LOCALE = "en_US"

loader = JsonLoader("./translations")
tr = PydanticI18n(loader)

def get_locale(locale: str = DEFAULT_LOCALE) -> str:
    return locale


async def validation_exception_handler(
        request: Request, exc: RequestValidationError
        ) -> JSONResponse:
    current_locale = request.query_params.get("locale", DEFAULT_LOCALE)
    return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": tr.translate(exc.errors(), current_locale)},
    )
