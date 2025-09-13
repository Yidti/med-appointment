# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port 8000 for Gunicorn
EXPOSE 8000

# Run gunicorn
# The actual command will be specified in docker-compose.yml
# This is just a placeholder if someone runs the container directly.
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "med_appointment.wsgi:application"]
