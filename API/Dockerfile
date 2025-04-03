# ----- Setup stage -----
FROM python:3.12 AS builder

# Set working directory
WORKDIR /app 

# Copy entire codebase into the container
COPY . .

# Install Poetry and add to PATH
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy pyproject.toml and poetry.lock first for caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi && \
    poetry add dynamic-frcm

# Expose port
EXPOSE 8080

# ----- Running stage -----
FROM python:3.12-alpine

# Create working directory and user
RUN addgroup -g 1000 app && \
    adduser -G app -D -u 1000 -h /app app

WORKDIR /app
USER app

# Copy app from setup stage
COPY --from=builder --chown=1000:1000 /app .

# Run the app
CMD ["python", "main.py"]
