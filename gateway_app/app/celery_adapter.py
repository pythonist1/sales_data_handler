from celery import Celery
from .abstractions import AbstractWorkerAdapter


class CeleryAdapter(AbstractWorkerAdapter):
    def __init__(self, celery_app: Celery):
        self._celery_app = celery_app

    def handle_file(self, file_id: str):
        result = self._celery_app.send_task(
            'tasks.handle_file',
            kwargs={'file_id': file_id}
        )
        return result.id

    def check_task_status(self, task_id: str):
        result = self._celery_app.AsyncResult(task_id, app=self._celery_app)
        if result.status == 'SUCCESS':
            return result.result
        else:
            return result.status

    def delete_task_case_with_countdown(self, file_id: str):
        self._celery_app.send_task(
            'tasks.delete_records',
            kwargs={'file_id': file_id},
            countdown=60
        )
