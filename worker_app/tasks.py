from app_module.bootstrap import bootstrap_celery_app, bootstrap_sales_data_handler


def get_handler():
    handler = bootstrap_sales_data_handler()
    return handler


app = bootstrap_celery_app()


@app.task()
def handle_file(file_id: str):
    handler = get_handler()
    result = handler.handle_sales_data(file_id=file_id)
    return result


@app.task()
def delete_records(file_id: str):
    handler = get_handler()
    result = handler.delete_records(file_id=file_id)
    return result
