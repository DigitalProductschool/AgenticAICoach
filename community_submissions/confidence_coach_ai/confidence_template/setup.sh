#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Install any dependencies (if needed - Poetry should handle this, but it's a good safety net)
# pip install -r requirements.txt  # If you have a requirements.txt file

# Activate the virtual environment (if you're using one - Poetry should handle this)
# source .venv/bin/activate  # Adjust path if needed

# Set the port for the API server (Heroku provides this in an environment variable)
export PORT="${PORT:-8000}"  # Default to 8000 if PORT is not set

# Start the API server in the background
python crewapi.py --port $PORT &
API_PID=$!  # Capture the process ID of the backgrounded API server

# Wait for the API server to start (optional, but recommended)
# A more robust check would be to poll the API endpoint
sleep 5

# Start the Streamlit app in the foreground.  This is CRUCIAL.  Heroku needs a foreground process.
streamlit run crew_app.py --server.port $PORT --server.enableCORS false
# Optionally, you can add --server.address 0.0.0.0 if needed, but usually not necessary

# Clean up the API server if the Streamlit app exits (optional)
# kill $API_PID 2>/dev/null || true # Ignore errors if the process doesn't exist