# Base Python image
FROM python:3.11-slim AS python-base

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    USE_DOCKER=1 \
    # Locale settings
    LANG=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8 \
    LC_TIME=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    # App path
    APP_PATH="/app"

ENV PATH="/root/.local/bin:$PATH"

###############################################
# Builder stage
###############################################
FROM python-base AS builder

# Install system dependencies and uv
RUN apt-get update && apt-get install --no-install-recommends -y \
      bash curl build-essential gcc \
  && curl -LsSf https://astral.sh/uv/install.sh | sh \
  && apt-get purge -y --auto-remove \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR $APP_PATH

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock* ./

# Install dependencies (without dev)
RUN uv sync --frozen --no-dev

###############################################
# Development stage
###############################################
FROM builder AS development

WORKDIR $APP_PATH

# Install dev dependencies
RUN uv sync --frozen

# Copy source code
COPY . .

# Run app with reload in dev (if needed inside main.py)
CMD ["python", "app/main.py"]

###############################################
# Production stage
###############################################
FROM builder AS production

WORKDIR $APP_PATH

# Copy source code
COPY . .

# Run app via python
CMD ["python", "app/main.py"]