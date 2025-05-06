# Use an official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first to cache Docker layers
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port that Cloud Run will use
EXPOSE 8080

# Start the app using uvicorn, make sure to use the PORT env variable
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
