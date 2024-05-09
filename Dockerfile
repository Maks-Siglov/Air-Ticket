FROM python:3.11.6-slim

RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc

WORKDIR /app

COPY requirements/prod.txt .
COPY requirements/tools.txt .

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install  --no-cache-dir --upgrade -r prod.txt -r tools.txt

RUN rm -rf /var/lib/apt/lists/*

COPY air_ticket air_ticket
