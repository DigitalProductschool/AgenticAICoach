FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /app

EXPOSE 8000

CMD ["poetry", "run", "chainlit", "run", "src/ai_branding_coach/main.py", "--host", "0.0.0.0", "-w"]