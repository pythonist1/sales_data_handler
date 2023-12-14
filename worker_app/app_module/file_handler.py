import os
import pathlib
import pandas as pd
from contextlib import suppress
from .settings import config
from .abstractions import AbstractFileHandler
from .exceptions import FileValidationError


file_apth = pathlib.Path(__file__).parent


class FileHandler(AbstractFileHandler):
    @staticmethod
    def extract_data_from_file(file_id: str):
        try:

            with open(config.file_path + file_id + '.xlsx', mode='rb') as file:
                file_data = file.read()

            data = pd.ExcelFile(file_data)
            sheet_names = data.sheet_names

            result = data.parse(sheet_names[0], na_filter=False)

            sales_data = dict()

            for i, row in result.iterrows():
                row_dict = row.to_dict()
                if not isinstance(row_dict['Date'], pd.Timestamp):
                    raise FileValidationError('Значение поля в столбце Date должно быть строкой в формате даты YYYY-MM-DD')
                try:
                    sales = float(row_dict['Sales'])
                except ValueError:
                    if row_dict['Sales'] == '':
                        sales = row_dict['Sales']
                    else:
                        raise FileValidationError('Значение поля в столбце Sales должно быть числом или пустым')
                sales_data[row_dict['Date'].date()] = sales
            if not sales_data:
                raise FileValidationError('Таблица пустая')
        except KeyError as exp:
            message = f'В таблице отсутствует столбец с названием {str(exp)}'
            raise FileValidationError(message)
        except Exception as exp:
            raise FileValidationError(str(exp))

        return sales_data

    @staticmethod
    def collect_file(sales_data: dict, file_id: str):
        sales_data_list = list()

        for key, value in sales_data.items():
            sales_data_item = dict()
            sales_data_item['Date'] = key
            sales_data_item['Sales'] = value
            sales_data_list.append(sales_data_item)

        df = pd.DataFrame(data=sales_data_list)

        path = config.file_path + file_id + '_result.xlsx'

        df.to_excel(path, index=False)

    @staticmethod
    def delete_files(file_id: str):
        with suppress(FileNotFoundError):
            paths = [
                config.file_path + file_id + '.xlsx',
                config.file_path + file_id + '_result.xlsx'
            ]

            for path in paths:
                os.remove(path)
