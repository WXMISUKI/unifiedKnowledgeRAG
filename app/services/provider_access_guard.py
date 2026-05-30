from collections.abc import Awaitable, Callable

from fastapi import Request
from fastapi.responses import JSONResponse, Response

from app.config import Settings, get_settings


UNAUTHORIZED_PROVIDER_ERROR = {
    "code": "PROVIDER_API_KEY_REQUIRED",
    "message": "A valid provider API key is required for this endpoint.",
}


async def provider_access_guard_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    settings = get_settings()
    if not _requires_provider_key(request, settings):
        return await call_next(request)
    if _request_has_valid_key(request, settings.provider_api_key):
        return await call_next(request)
    return JSONResponse(
        status_code=401,
        content={
            "ok": False,
            "error": UNAUTHORIZED_PROVIDER_ERROR,
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


def _requires_provider_key(request: Request, settings: Settings) -> bool:
    return bool(settings.provider_api_key) and request.url.path.startswith("/api/")


def _request_has_valid_key(request: Request, expected_key: str | None) -> bool:
    if expected_key is None:
        return True
    return (
        _bearer_token(request.headers.get("authorization")) == expected_key
        or request.headers.get("x-provider-api-key") == expected_key
    )


def _bearer_token(header_value: str | None) -> str | None:
    if not header_value:
        return None
    scheme, _, token = header_value.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token
