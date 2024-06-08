# Use the official Python image from the Docker Hub
ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set the working directory for the app
WORKDIR /app

# Create a non-privileged user that the app will run under
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Switch to the non-privileged user to run the application
USER appuser

# Copy the application code into the container
COPY . .

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
