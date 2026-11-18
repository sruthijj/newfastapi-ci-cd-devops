# Use lightweight official Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files and keep output unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port 80 to match Kubernetes manifest
EXPOSE 80

# Start Uvicorn server on port 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
