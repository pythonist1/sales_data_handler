from uuid import uuid4
from worker_app.app.bootstrap import bootstrap_repository


def test_repository_log_error():
    repository = bootstrap_repository()
    repository.log_error('description')

def test_repository_delete_records():
    repository = bootstrap_repository()
    repository.delete_task_case('b8a5d007-25a6-472b-8613-fc7c05a4f8db')
