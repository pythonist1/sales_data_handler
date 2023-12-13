import uvicorn
from fastapi import FastAPI
from .settings import config
from .gateway.exception_handler import base_exception_handler
from .gateway.api import router


app = FastAPI(
    docs_url=config.docs_url,
    exception_handlers={
        Exception: base_exception_handler
    }
)

app.include_router(router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
