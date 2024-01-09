from fastapi import APIRouter
from applications.api.health_check.handler import router as health_check_router

v1 = APIRouter(prefix='/api')

v1.include_router(health_check_router, prefix='/healthcheck', tags=['health_check'])
