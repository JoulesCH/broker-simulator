FROM python:3.9.5-slim-buster

WORKDIR /app

ADD . /app

RUN pip install wheel

RUN pip install -r requirements.txt

CMD python run.py