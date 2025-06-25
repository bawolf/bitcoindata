# Use the official Python lightweight image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables for the container
# The PORT environment variable is set by Cloud Run to tell the container which port to listen on.
# Default to 8080 for local testing with Docker.
ENV PORT=8080

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED=1

# Install uv by copying the binary from the official Astral image.
# This is the recommended, most robust method for containers.
# See: https://cloud.google.com/blog/topics/developers-practitioners/build-and-deploy-a-remote-mcp-server-to-google-cloud-run-in-under-10-minutes
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy all project files into the container.
# This ensures that build dependencies like README.md are available.
COPY . .

# Install project dependencies. uv will create a virtual environment in /app/.venv
RUN uv sync --extra web

# Expose the port that the application will listen on
EXPOSE 8080

# Define the command to run the application using the virtual environment's gunicorn.
# Use the shell form of CMD to allow shell variable expansion for $PORT.
CMD .venv/bin/gunicorn --workers 2 --bind "0.0.0.0:$PORT" web_deployment_example:app 