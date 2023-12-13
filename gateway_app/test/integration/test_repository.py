from uuid import uuid4
from gateway_app.app.repository import Repository
from gateway_app.app.bootstrap import bootstrap_database_engine


async def test_repository():
    engine = bootstrap_database_engine()
    repository = Repository(db_engine=engine)

    task_id = str(uuid4())
    file_id = str(uuid4())

    print(task_id)
    print(file_id)

    await repository.create_task_case(task_id, file_id)
