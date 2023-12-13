import os
import pathlib
import random
import pandas as pd
from pprint import pprint
from uuid import uuid4
from datetime import date, timedelta
from worker_app.app.file_handler import FileHandler
from worker_app.app.fake_sales_service_adapter.adapter import FakeSalesServiceAdapter

from worker_app.app.settings import config


file_apth = pathlib.Path(__file__).parent


async def test_extract_file():
    sales_data = FileHandler.extract_data_from_file(file_id='sales')

    FileHandler.collect_file(sales_data=sales_data, file_id='sales')


async def test_create_file():
    d = date(2023, 2, 1)

    dates = list()

    for i in range(10):
        sales_date = d + timedelta(days=i)
        dates.append(sales_date)

    sales_data_list = list()

    for date_ in dates:
        sales_data_item = dict()
        sales_data_item['Date'] = date_
        sales_data_item['Sales'] = round(random.uniform(0, 1000000), 2)
        sales_data_list.append(sales_data_item)

    df = pd.DataFrame(data=sales_data_list)

    file_case_id = str(uuid4())

    print(config.file_path)
    path = config.file_path + f'{file_case_id}.xlsx'

    print(path)
    df.to_excel(path, index=False)


async def test_fake_sales_service_adapter():
    d = date(2023, 2, 1)

    dates = list()

    for i in range(10):
        sales_date = d + timedelta(days=i)
        dates.append(sales_date)

    adapter = FakeSalesServiceAdapter()

    sales_data = adapter.get_sales_by_dates(dates)
    pprint(sales_data)


async def test_celery():
    from celery import Celery
    from time import sleep
    from datetime import datetime, timedelta
    app = Celery('app_', broker='redis://localhost:6379', backend='redis://localhost:6379')

    result = app.send_task(
        'app.celery.handle_file',
        kwargs={'file_id': 'b8a5d007-25a6-472b-8613-fc7c05a4f8db'}
    )

    print(result.id)
    print(result.status)


    sleep(2)
    result_ = app.AsyncResult(result.id, app=app)
    print(result_.status)
    print(result_.result)

    result = app.send_task(
        'app.celery.delete_records',
        kwargs={'file_id': 'sales'},
        countdown=2
    )

    sleep(3)
    result_ = app.AsyncResult(result.id, app=app)
    print(result_.status)
    print(result_.result)
