from typing import Type
from .abstractions import AbstractFileHandler, AbstractRepository, AbstractSalesServiceAdapter
from .model import Sales
from .exceptions import BaseDataHandlerException


class SalesDataHandler:
    def __init__(self,
                 file_handler: Type[AbstractFileHandler],
                 repository: AbstractRepository,
                 sales_service_adapter: AbstractSalesServiceAdapter):
        self._file_handler = file_handler
        self._repository = repository
        self._sales_service_adapter = sales_service_adapter

    def handle_sales_data(self, file_id: str) -> dict:
        try:
            result = self._handle_sales_data(file_id)
            return result
        except BaseDataHandlerException as exp:
            self._repository.log_error(description=str(exp), file_id=file_id)
            return {
                'status': 'ERROR',
                'message': str(exp)
            }
        except Exception as exp:
            return {
                'status': 'ERROR',
                'message': str(exp)
            }

    def _handle_sales_data(self, file_id: str) -> dict:
        sales_data = self._file_handler.extract_data_from_file(file_id=file_id)
        sales = Sales(sales_data=sales_data)

        if sales.empty_dates:
            additional_data = self._sales_service_adapter.get_sales_by_dates(
                dates=sales.empty_dates
            )
            sales.complete_empty_data(additional_data=additional_data)

        self._file_handler.collect_file(
            sales_data=sales.sales_data,
            file_id=file_id
        )

        return {
            'status': 'SUCCESS',
        }

    def delete_records(self, file_id: str):
        try:
            self._file_handler.delete_files(file_id=str(file_id))
            self._repository.delete_task_case(file_id=file_id)

            return {
                'status': 'SUCCESS',
            }

        except Exception as exp:
            return {
                'status': 'ERROR',
                'message': str(exp)
            }
