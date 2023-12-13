FROM python:latest

COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /gateway_app
WORKDIR /gateway_app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
