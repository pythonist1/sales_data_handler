from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from celery import Celery
from .settings import config
from . import Repository, SalesDataHandler, FileHandler, FakeSalesServiceAdapter, metadata


def bootstrap_db_session_maker():
    username = config.postgres_user
    password = config.postrges_password
    host = config.postgres_server
    port = config.postgres_port
    db_name = config.postgres_db
    database_url = f"postgresql://{username}:{password}@{host}:{port}/postgres"
    engine = create_engine(database_url, isolation_level='AUTOCOMMIT')

    create_database_stmt = text('CREATE DATABASE sales_worker')
    try:
        with engine.connect() as connection:
            connection.execute(create_database_stmt)
    except:
        pass

    database_url = f"postgresql://{username}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(database_url)
    metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine, autoflush=False)
    return session_maker


session_maker = bootstrap_db_session_maker()


def get_db_session():
    session = session_maker()
    try:
        yield session
    finally:
        session.close()


def bootstrap_repository() -> Repository:
    session = next(get_db_session())
    repository = Repository(db_session=session)
    return repository


def bootstrap_sales_data_handler() -> SalesDataHandler:
    repository = bootstrap_repository()
    sales_service_adapter = FakeSalesServiceAdapter()

    handler = SalesDataHandler(
        file_handler=FileHandler,
        repository=repository,
        sales_service_adapter=sales_service_adapter
    )

    return handler


def bootstrap_celery_app():
    REDIS_URL = f'redis://{config.redis_host}:{config.redis_port}/0'

    app = Celery(
        'tasks',
        broker=REDIS_URL,
        backend=REDIS_URL
    )

    return app
