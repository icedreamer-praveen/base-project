FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Kathmandu /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update -y && apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y python3.10 python3-distutils python3-pip python3-apt
RUN apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential default-libmysqlclient-dev mysql-client

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

ADD . /app
WORKDIR /app

COPY requirements.txt ./
COPY . ./ 
RUN pip install --upgrade pip && \
    pip install --upgrade setuptools
RUN pip --no-cache-dir install -r requirements.txt


EXPOSE 8000


CMD ["sh", "-c", "python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]

