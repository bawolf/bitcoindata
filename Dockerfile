# Multi-stage build: Frontend (React/TypeScript) + Backend (Python)

# Stage 1: Build React/TypeScript frontend
FROM node:18-alpine AS frontend
WORKDIR /app

# Copy package files for dependency installation
COPY package*.json ./
COPY tsconfig*.json ./
COPY tailwind.config.js postcss.config.js ./

# Install Node.js dependencies (including dev dependencies for build)
RUN npm ci

# Copy source code and build
COPY src/ ./src/
COPY index.html ./
COPY vite.config.js ./

# Build the React/TypeScript application
RUN npm run build

# Stage 2: Python backend with built frontend
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

# Copy built React files from frontend stage
COPY --from=frontend /app/static/dist ./static/dist

# Copy Python project files
COPY pyproject.toml uv.lock ./
COPY README.md ./
COPY *.py ./
COPY templates/ ./templates/

# Install Python dependencies. uv will create a virtual environment in /app/.venv
RUN uv sync --extra web

# Expose the port that the application will listen on
EXPOSE 8080

# Define the command to run the application using the virtual environment's gunicorn.
# The --preload flag loads application code before forking workers.
# This ensures that one-time initialization (like data download) happens only once.
CMD [".venv/bin/gunicorn", "--workers", "2", "--bind", "0.0.0.0:8080", "--preload", "web_deployment_example_react:app"] 