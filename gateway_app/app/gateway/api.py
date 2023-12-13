from fastapi import APIRouter, UploadFile, File
from starlette.responses import JSONResponse, FileResponse
from ..bootstrap import bootstrap_task_handler


handler = bootstrap_task_handler()
router = APIRouter()


@router.post('/handle_file/')
async def handle_file(file: UploadFile = File(...)):
    file_data = await file.read()
    task_id = await handler.handle_excel_file(
        file_data=file_data,
        filename=file.filename
    )
    return JSONResponse(
        status_code=200,
        content={'status': 'SUCCESS', 'task_id': task_id}
    )


@router.get('/check_status/{task_id}/')
async def check_task_status(task_id: str):
    task_status = await handler.check_task_status(task_id=task_id)
    return JSONResponse(
        status_code=200,
        content={'task_status': task_status}
    )


@router.get('/get_result_file/{task_id}/')
async def get_file(task_id: str):
    filepath, filename = await handler.get_task_result(task_id=task_id)

    return FileResponse(
        filepath,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename=filename
    )
