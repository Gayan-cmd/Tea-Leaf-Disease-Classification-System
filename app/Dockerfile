# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend application code
COPY app/ app/

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the application
# We set the server.address to 0.0.0.0 so it is accessible from outside the container
CMD ["streamlit", "run", "app/frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
