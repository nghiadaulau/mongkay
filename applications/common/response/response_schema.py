#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict

from applications.common.response.response_code import CustomResponse, CustomResponseCode
from applications.core.settings import settings

_ExcludeData = Union[set[Union[int, str]], dict[Union[int, str], Any]]

__all__ = ['ResponseModel', 'response_base']


class ResponseModel(BaseModel):
    # TODO: json_encoders 配置失效: https://github.com/tiangolo/fastapi/discussions/10252
    model_config = ConfigDict(json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)})

    code: int = CustomResponseCode.HTTP_200.code
    message: str = CustomResponseCode.HTTP_200.message
    data: Union[Any, None] = None


class ResponseBase:
    @staticmethod
    async def __response(
            *,
            res: Union[CustomResponseCode, CustomResponse] = None,
            data: Union[Any, None] = None,
            exclude: Union[_ExcludeData, None] = None,
            **kwargs,
    ) -> dict:
        """
        :param code: http status code
        :param message: body message
        :param data: response data
        :param exclude: exclude
        :param kwargs: jsonable_encoder
        :return:
        """
        if data is not None:
            # TODO: custom_encoder : https://github.com/tiangolo/fastapi/discussions/10252
            custom_encoder = {datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)}
            kwargs.update({'custom_encoder': custom_encoder})
            data = jsonable_encoder(data, exclude=exclude, **kwargs)
        return {'code': res.code, 'message': res.message, 'data': data}

    async def success(
            self,
            *,
            res: Union[CustomResponseCode, CustomResponse] = CustomResponseCode.HTTP_200,
            data: Union[Any, None] = None,
            exclude: Union[_ExcludeData, None] = None,
            **kwargs,
    ) -> dict:
        return await self.__response(res=res, data=data, exclude=exclude, **kwargs)

    async def fail(
            self,
            *,
            res: Union[CustomResponseCode, CustomResponse] = CustomResponseCode.HTTP_400,
            data: Any = None,
            exclude: Union[_ExcludeData, None],
            **kwargs,
    ) -> dict:
        return await self.__response(res=res, data=data, exclude=exclude, **kwargs)


response_base = ResponseBase()