from fastapi import FastAPI
from applications.core.settings import settings
from fastapi.middleware.trustedhost import TrustedHostMiddleware


def register_app():
    app = FastAPI()
    register_middleware(app)

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


