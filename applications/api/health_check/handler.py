from fastapi import APIRouter

from applications.common.response.response_schema import response_base

router = APIRouter()


@router.get('/all')
async def get_all_apis():
    data = {"message": "Hello World"}
    return await response_base.success(data=data)
