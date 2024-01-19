import uvicorn
from path import Path
from applications.core.registrator import register_app
from applications.core.settings import settings
from applications.common.log_lib import LogMessage

app = register_app()
logger = LogMessage()

if __name__ == '__main__':
    try:
        uvicorn.run(
            app=f'{Path(__file__).stem}:app',
            host=settings.UVICORN_HOST,
            port=settings.UVICORN_PORT,
            reload=settings.UVICORN_RELOAD,
            log_config=settings.LOGGING,
            access_log=False
        )
    except Exception as e:
        logger.debug(f'FastAPI start filed: {e}')
