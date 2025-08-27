FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc git curl ca-certificates libsasl2-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements first for caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project
COPY . /app

# create non-root user
RUN useradd -m -s /bin/bash appuser && chown -R appuser:appuser /app
USER appuser

# Expose app port (nginx will be in front)
EXPOSE 8000

# Use gunicorn with uvicorn workers for production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "api.server:app", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "120"]
