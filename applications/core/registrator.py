from http.client import HTTPException
from fastapi import Depends, FastAPI, Request
from starlette.responses import JSONResponse

from applications.core.settings import settings
from applications.api.routers import v1
from fastapi.middleware.trustedhost import TrustedHostMiddleware


def register_app():
    app = FastAPI()
    register_middleware(app)
    register_router(app)
    register_exception_handler(app)
    return app


def register_middleware(app: FastAPI):
    """
    :param app:
    :return:
    """

    # TrustedHostMiddleware: Accept selected hosts.
    app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS
    )

    # Gzip: Always at the top
    if settings.MIDDLEWARE_GZIP:
        from fastapi.middleware.gzip import GZipMiddleware
        app.add_middleware(GZipMiddleware)

    # CORS: Always at the end
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_router(app: FastAPI):
    """
    :param app: FastAPI
    :return:
    """
    # API
    app.include_router(v1)


def register_exception_handler(app: FastAPI):
    """
    :param app: FastAPI
    :return:
    """
    app.add_exception_handler(404, not_found_error)


def not_found_error(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"message": "Oops! The resource you requested was not found."},
    )
