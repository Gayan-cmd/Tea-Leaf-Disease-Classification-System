# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies required for some Python packages (e.g., Pillow, OpenCV if added later)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY api/ api/
COPY src/ src/
COPY models/ models/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
