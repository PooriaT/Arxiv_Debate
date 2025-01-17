# Use the official Python image as the base image
FROM python:3.13.1-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.5

# Install system dependencies required by Poetry and Streamlit
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry package manager
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory inside the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry install --no-root --no-dev

# Copy the entire project into the working directory
COPY . .

# Expose the default Streamlit port
EXPOSE 8501

# Set the entrypoint command to run Streamlit
#CMD ["poetry", "run", "streamlit", "run", "app/main.py"]