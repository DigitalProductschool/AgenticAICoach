# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose ports
EXPOSE 8000 8501

# Create a startup script
RUN echo '#!/bin/bash\nuvicorn main:app --host 0.0.0.0 --port 8000 &\nstreamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless=true' > start.sh
RUN chmod +x start.sh

# Start both services
CMD ["/bin/bash","./start.sh"]
