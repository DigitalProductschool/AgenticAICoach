# Use the official Python image
FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "src.cv_reviewer.app.api:app", "--host", "0.0.0.0", "--port", "8000"]
