from abc import ABC, abstractmethod



class AbstractWorkerAdapter(ABC):
    @abstractmethod
    def handle_file(self, file_id: str):
        pass

    @abstractmethod
    def check_task_status(self, task_id: str):
        pass

    @abstractmethod
    def delete_task_case_with_countdown(self, file_id: str):
        pass


class AbstractRepository(ABC):
    @abstractmethod
    async def create_task_case(self, task_id: str, file_id: str, filename: str):
        pass

    @abstractmethod
    async def save_file(self, file_data: bytes, file_id: str):
        pass

    @abstractmethod
    async def get_file_data(self, task_id: str):
        pass
