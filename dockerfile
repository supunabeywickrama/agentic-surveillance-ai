# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for OpenCV and YOLO
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the image
COPY . /app/

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Command to run both the FastAPI backend and Streamlit dashboard
# Using a simple shell entry to launch both natively. In a production cluster
# you would split these into separate containers managed by docker-compose.
CMD uvicorn backend.api:app --host 0.0.0.0 --port 8000 & streamlit run dashboard/dashboard_server.py --server.port 8501 --server.address 0.0.0.0
