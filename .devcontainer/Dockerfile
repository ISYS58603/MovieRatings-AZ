# Example Dockerfile for a production-ready Flask app
FROM python:3.13.0-bullseye

# Set up the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Environment variables
ENV PORT 8000

# Start the app using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:create_app()"]
