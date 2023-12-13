import random
from .. import AbstractSalesServiceAdapter


class FakeSalesServiceAdapter(AbstractSalesServiceAdapter):
    def get_sales_by_dates(self, dates: list):
        sales = self._fake_request(dates)
        return sales

    def _fake_request(self, dates: list):
        sales = dict()

        for sale_date in dates:
            sales[sale_date] = round(random.uniform(0, 1000000), 2)

        return sales
