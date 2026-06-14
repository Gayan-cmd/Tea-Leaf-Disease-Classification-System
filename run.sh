#!/bin/bash

# Start the FastAPI backend in the background
uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# Wait a few seconds for the backend to spin up
sleep 3

# Start the Streamlit frontend. 
# Hugging Face exposes port 7860 to the public, so Streamlit must run there.
streamlit run app/frontend.py --server.port=7860 --server.address=0.0.0.0 --server.enableCORS=false --server.enableXsrfProtection=false
