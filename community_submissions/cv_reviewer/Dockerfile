# --- Stage 1: build with pip ---
FROM python:3.11-slim AS builder
WORKDIR /app

# copy requirements and install
COPY requirements.txt ./
RUN pip install -r requirements.txt

# --- Stage 2: final image ---
FROM python:3.11-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# bring in installed packages
COPY --from=builder /usr/local/lib/python3.11/site-packages \
     /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# app code + env
COPY ./src ./src
COPY ./static ./static
COPY .env .env

EXPOSE 8000
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "4", "-b", "0.0.0.0:8000", "src.api:app"]
