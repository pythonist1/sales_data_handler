import os
import aiofiles
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

from .abstractions import AbstractRepository
from .settings import config


class Repository(AbstractRepository):
    def __init__(self, db_engine: AsyncEngine):
        self._engine = db_engine

    async def create_task_case(self, task_id: str, file_id: str, filename: str):
        insert_stmt = text('''
            INSERT INTO task_case (task_id, file_id, filename)
            VALUES (:task_id, :file_id, :filename)
            RETURNING id
        ''')

        async with self._engine.begin() as connection:
            await connection.execute(
                insert_stmt,
                {
                    'task_id': task_id,
                    'file_id': file_id,
                    'filename': filename
                }
            )
            await connection.commit()

    async def save_file(self, file_data: bytes, file_id: str):
        filepath = os.path.join(config.file_path, str(file_id) + '.xlsx')
        async with aiofiles.open(filepath, mode='wb') as file:
            await file.write(file_data)

    async def get_file_data(self, task_id: str):
        select_stmt = text('''
            SELECT file_id, filename
            FROM task_case
            WHERE task_id = :task_id
        ''')
        async with self._engine.begin() as connection:
            result = (await connection.execute(
                select_stmt,
                {'task_id': task_id}
            )).first()
        file_id = result.file_id
        filename = result.filename
        filepath = os.path.join(config.file_path, str(file_id) + '_result.xlsx')

        return file_id, filepath, filename
