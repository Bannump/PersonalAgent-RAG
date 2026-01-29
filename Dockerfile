FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set Python path to include the app directory
ENV PYTHONPATH=/app

# Expose port (Railway uses PORT env variable)
EXPOSE 8000

# Start the application - use shell form to support $PORT
CMD uvicorn backend.api:app --host 0.0.0.0 --port ${PORT:-8000}
