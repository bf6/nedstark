FROM python:2

ARG BOT_ACCESS_TOKEN

RUN mkdir -p /src/app
COPY requirements.txt /src/app
WORKDIR /src/app
RUN pip install -r requirements.txt

COPY . /src/app

ENV BOT_ACCESS_TOKEN=$BOT_ACCESS_TOKEN

EXPOSE 8000

RUN gunicorn app:api
