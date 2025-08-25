# Use the official Python image as the base image
FROM python:3.13-alpine

# Set the working directory within the container
WORKDIR /app

# Copy the application code into the container
COPY app.py docker-logo.png requirements.txt ./

# Install Flask and other dependencies
RUN pip install --upgrade pip && \
	pip install -r requirements.txt

# Expose port 8080 to the host
EXPOSE 8080

# Define the command to run the application
ENTRYPOINT ["python", "app.py"]
