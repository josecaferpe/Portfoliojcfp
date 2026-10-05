FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos '' sysadmin

RUN mkdir -p /app/logs && chown -R sysadmin:sysadmin /app/logs

USER sysadmin

CMD ["python", "monitor.py"]
