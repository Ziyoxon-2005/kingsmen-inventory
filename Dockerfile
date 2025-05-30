# Base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 