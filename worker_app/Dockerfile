FROM python:latest

COPY requirements.txt /
RUN pip install -r /requirements.txt

ADD . /worker_app
WORKDIR /worker_app

ENTRYPOINT celery -A tasks worker --loglevel=info
