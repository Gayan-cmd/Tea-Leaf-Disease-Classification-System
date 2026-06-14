# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements files
COPY api/requirements.txt api_requirements.txt
COPY app/requirements.txt app_requirements.txt

# Install dependencies for both backend and frontend
RUN pip install --no-cache-dir -r api_requirements.txt
RUN pip install --no-cache-dir -r app_requirements.txt

# Copy the rest of the application code
COPY api/ api/
COPY app/ app/
COPY src/ src/
COPY models/ models/
COPY run.sh run.sh

# Make the startup script executable
RUN chmod +x run.sh

# Expose the Hugging Face Spaces port
EXPOSE 7860

# Command to run both the API and Streamlit
CMD ["./run.sh"]
