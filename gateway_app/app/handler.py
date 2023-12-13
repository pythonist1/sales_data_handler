from uuid import uuid4
from .abstractions import AbstractRepository, AbstractWorkerAdapter


class TasksHandler:
    def __init__(self, repository: AbstractRepository, worker_adapter: AbstractWorkerAdapter):
        self._repository = repository
        self._worker_adapter = worker_adapter

    async def handle_excel_file(self, file_data: bytes, filename: str):
        file_id = str(uuid4())
        await self._repository.save_file(file_data=file_data, file_id=file_id)
        task_id = self._worker_adapter.handle_file(file_id=file_id)
        await self._repository.create_task_case(
            task_id=task_id,
            file_id=file_id,
            filename=filename
        )
        return task_id

    async def check_task_status(self, task_id: str):
        task_status = self._worker_adapter.check_task_status(task_id=task_id)
        return task_status

    async def get_task_result(self, task_id: str):
        file_id, filepath, filename = await self._repository.get_file_data(task_id=task_id)
        self._worker_adapter.delete_task_case_with_countdown(file_id=file_id)
        return filepath, filename
