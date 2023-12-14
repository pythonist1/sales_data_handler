from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import delete, select, update
from ..abstractions import AbstractRepository
from .tables import ErrorLog, TaskCase


class Repository(AbstractRepository):
    def __init__(self, db_session: Session):
        self._session = db_session

    def log_error(self, description: str, file_id: str):
        update_stmt = update(TaskCase).where(TaskCase.file_id == file_id)\
            .values({'status': 'ERROR'}).returning(TaskCase.task_id)
        task_id = (self._session.execute(update_stmt)).scalar()
        error_log = ErrorLog(
            id=uuid4(),
            task_id=task_id,
            error_time=datetime.now(),
            description=description
        )
        self._session.add(error_log)
        self._session.commit()

    def delete_task_case(self, file_id: str):
        delete_stmt = delete(TaskCase).where(TaskCase.file_id == file_id)
        self._session.execute(delete_stmt)
        self._session.commit()
