# Build the React frontend
FROM node:20 as frontend

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Use an official Python runtime as a parent image for the Flask backend
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the built React frontend to the static folder
COPY --from=frontend /app/frontend/build /app/thehighlander/static

# Create a directory for logs inside the container if it doesn't exist
RUN mkdir -p /app/logs

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 2121 available to the world outside this container
EXPOSE 2121

# Set an environment variable for the log file path
ENV LOG_FILE /app/logs/gunicorn.log

# Run app.py using Gunicorn when the container launches and store logs in the log file
CMD ["gunicorn", "thehighlander:app", "-b", "0.0.0.0:2121", "--access-logfile", "${LOG_FILE}", "--error-logfile", "${LOG_FILE}", "--log-level", "debug"]
