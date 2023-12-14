import os
import aiofiles
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

from .abstractions import AbstractRepository
from .exceptions import TaskCaseException
from .settings import config


class Repository(AbstractRepository):
    def __init__(self, db_engine: AsyncEngine):
        self._engine = db_engine

    async def create_task_case(self, task_id: str, file_id: str, filename: str):
        async with self._engine.begin() as connection:
            await connection.execute(
                Statements.insert_task_case_stmt,
                {
                    'task_id': task_id,
                    'file_id': file_id,
                    'filename': filename,
                    'status': 'PENDING'
                }
            )
            await connection.commit()

    async def save_file(self, file_data: bytes, file_id: str):
        filepath = os.path.join(config.file_path, str(file_id) + '.xlsx')
        async with aiofiles.open(filepath, mode='wb') as file:
            await file.write(file_data)

    async def get_file_data(self, task_id: str):
        async with self._engine.begin() as connection:
            result = (await connection.execute(
                Statements.select_task_case_stmt,
                {'task_id': task_id}
            )).first()

        if result.status == 'ERROR':
            async with self._engine.begin() as connection:
                result = (await connection.execute(
                    Statements.select_error_log_stmt,
                    {'task_id': task_id}
                )).first()
                raise TaskCaseException(result.description)

        file_id = result.file_id
        filename = result.filename
        filepath = os.path.join(config.file_path, str(file_id) + '_result.xlsx')

        return file_id, filepath, filename


class Statements:
    insert_task_case_stmt = text('''
        INSERT INTO task_case (task_id, file_id, filename)
        VALUES (:task_id, :file_id, :filename)
        RETURNING id
    ''')

    select_task_case_stmt = text('''
        SELECT file_id, filename, status
        FROM task_case
        WHERE task_id = :task_id
    ''')

    select_error_log_stmt = text('''
        SELECT description
        FROM error_log
        WHERE task_id = :task_id
    ''')
