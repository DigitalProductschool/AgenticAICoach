#!/bin/bash

# Start the API server in the background
python crewapi.py &

# Wait for the API server to start (optional, but recommended)
# You might need to adjust this based on how your API server starts
sleep 5

# Start the Streamlit app
streamlit run crew_app.py