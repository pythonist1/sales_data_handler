from fastapi import Request
from starlette.responses import JSONResponse
from ..exceptions import BaseGatewayAppException


async def base_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            'status': "ERROR",
            'data': {},
            'code': f'InternalServiceError {type(exc).__name__}',
            'detail': str(exc),
        }
    )

async def gateway_app_exception_handler(request: Request, exc: BaseGatewayAppException):
    return JSONResponse(
        status_code=422,
        content={
            'status': "ERROR",
            'data': {},
            'code': type(exc).__name__,
            'detail': str(exc.detail),
        }
    )
