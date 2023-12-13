from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def log_error(self, description: str):
        pass

    @abstractmethod
    def delete_task_case(self, file_id: str):
        pass


class AbstractSalesServiceAdapter(ABC):
    @abstractmethod
    def get_sales_by_dates(self, dates: list):
        pass


class AbstractFileHandler(ABC):
    @staticmethod
    @abstractmethod
    def extract_data_from_file(file_id: str):
        pass

    @staticmethod
    @abstractmethod
    def collect_file(sales_data: dict, file_id: str):
        pass

    @staticmethod
    @abstractmethod
    def delete_files(file_id: str):
        pass
