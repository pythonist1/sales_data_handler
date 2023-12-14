from sqlalchemy import Column, DateTime, String, UUID, Integer
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


metadata = Base.metadata


class ErrorLog(Base):
    __tablename__ = 'error_log'
    id = Column(UUID, primary_key=True, unique=True)
    task_id = Column(UUID, nullable=False)
    error_time = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)


class TaskCase(Base):
    __tablename__ = 'task_case'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    task_id = Column(UUID, unique=True, nullable=False)
    file_id = Column(UUID, unique=True, index=True, nullable=False)
    filename = Column(String, nullable=False)
    status = Column(String)
