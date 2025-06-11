FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv pip install --system -r pyproject.toml "gunicorn"

COPY . .

EXPOSE 8000

# Command to run the application using Gunicorn
# This is a production-ready web server
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "api:app"]
