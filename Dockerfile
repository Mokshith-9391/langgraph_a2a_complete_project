FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --retries 10 --timeout 120 -r requirements.txt

COPY common ./common
COPY agents ./agents
COPY supervisor ./supervisor
COPY client.py .
COPY README.md .

ENV PYTHONUNBUFFERED=1
