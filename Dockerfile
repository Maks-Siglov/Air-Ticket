FROM python:3.11.6-slim

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

COPY requirements/prod.txt .
COPY requirements/tools.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install  --no-cache-dir --upgrade -r prod.txt -r tools.txt


WORKDIR /air_ticket

COPY air_ticket .
