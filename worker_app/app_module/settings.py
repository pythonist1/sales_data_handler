import pathlib
from pydantic_settings import BaseSettings


project_path = pathlib.Path(__file__).parent
env_path = str(project_path) + '/.env'


class Config(BaseSettings):
    redis_host: str = 'host.docker.internal'
    redis_port: int = 6380
    postgres_user: str = 'postgres'
    postrges_password: str = 'postgres'
    postgres_server: str = 'host.docker.internal'
    postgres_port: int = 5434
    postgres_db: str = 'sales_worker'
    file_path: str = str(project_path) + '/files/'


config = Config(_env_file=env_path)
