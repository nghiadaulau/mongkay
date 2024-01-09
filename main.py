import uvicorn
from path import Path
from applications.core.registrator import register_app
from applications.core import settings
from applications.common.log_lib import Logger

app = register_app()
logger = Logger().logger


@app.get("/")
async def root():
    logger.debug("hello")
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    try:
        uvicorn.run(
            app=f'{Path(__file__).stem}:app',
            host=settings.UVICORN_HOST,
            port=settings.UVICORN_PORT,
            reload=settings.UVICORN_RELOAD,
        )
    except Exception as e:
        logger.info(f'FastAPI start filed: {e}')
