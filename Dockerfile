FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

RUN apt update

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /code/
