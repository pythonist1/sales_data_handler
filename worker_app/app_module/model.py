

class Sales:
    def __init__(self, sales_data: dict):
        self._sales_data = sales_data
        self._empty_dates = list()
        self._check_sales_data()

    @property
    def sales_data(self):
        return self._sales_data

    @property
    def empty_dates(self):
        return self._empty_dates

    def _check_sales_data(self):
        for date, sales in self._sales_data.items():
            if sales == '':
                self._empty_dates.append(date)

    def complete_empty_data(self, additional_data: dict):
        for date, sales in additional_data.items():
            self._sales_data[date] = sales
