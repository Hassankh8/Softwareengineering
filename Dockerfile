# Use official Python image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Copy project files to container
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r mediahub/requirements.txt

# Expose port (same as runserver port)
EXPOSE 8001

# Start Django server
CMD ["python", "mediahub/manage.py", "runserver", "0.0.0.0:8001"]
