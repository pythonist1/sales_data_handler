from celery import Celery
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from .settings import config
from .repository import Repository
from .celery_adapter import CeleryAdapter
from .handler import TasksHandler


def bootstrap_database_engine():
    username = config.postgres_user
    password = config.postrges_password
    host = config.postgres_server
    port = config.postgres_port
    db_name = config.postgres_db

    postgres_url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}"

    engine = create_async_engine(postgres_url)
    return engine


def bootstrap_celery_app():
    REDIS_URL = f'redis://{config.redis_host}:{config.redis_port}'

    app = Celery(
        'gateway_app',
        broker=REDIS_URL,
        backend=REDIS_URL
    )

    return app


def bootstrap_task_handler():
    engine = bootstrap_database_engine()
    celery_app = bootstrap_celery_app()
    repository = Repository(db_engine=engine)
    worker_adapter = CeleryAdapter(celery_app=celery_app)
    handler = TasksHandler(repository=repository, worker_adapter=worker_adapter)
    return handler
