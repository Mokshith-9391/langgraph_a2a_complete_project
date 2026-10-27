FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY agents ./agents
COPY supervisor ./supervisor
COPY client.py .
COPY README.md .

ENV PYTHONUNBUFFERED=1
