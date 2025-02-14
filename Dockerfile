# Use the official Python image as the base image
FROM python:3.13.1-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.8.5 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYTHONPATH="/app" \ 
    HOST="0.0.0.0" \
    PORT="8050"

# Install system dependencies required by Poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry package manager
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${POETRY_HOME}/bin:$PATH"

# Set the working directory inside the container
WORKDIR /app

# Copy only dependency files first for better caching
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the entire project
COPY . .

# Set proper permissions
RUN chmod -R 755 /app

# Expose the port the app will use
EXPOSE 8050

# Run the app when the container starts
CMD ["poetry", "run", "python", "app", "--host", "0.0.0.0"]
