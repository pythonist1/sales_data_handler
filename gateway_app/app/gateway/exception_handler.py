from fastapi import Request
from starlette.responses import JSONResponse


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
