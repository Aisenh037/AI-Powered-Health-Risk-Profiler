# Use an official, lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies if needed (e.g., for certain ML ops)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project structure
COPY . .

# Train models during build to ensure the image is ready-to-run
# This ensures ml_models and data are used correctly
RUN python ml_models/dataset_generator.py && python ml_models/model_trainer.py

# Expose the port (Render handles this dynamically, but good for documentation)
EXPOSE 10000

# Command to run the application
# Use the PORT environment variable provided by Render
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}
