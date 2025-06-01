FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose port
EXPOSE 8003

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"] 