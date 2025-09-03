FROM python:3.11-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    USE_DOCKER=1 \
    # uv settings
    UV_LINK_MODE=copy \
    # Locale settings
    LANG=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8 \
    LC_TIME=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    # paths
    UV_VENV="/opt/venv"

ENV PATH="$UV_VENV/bin:$PATH"

###############################################
# Builder Image
###############################################
FROM python-base AS builder-base

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    gcc \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies with uv
RUN uv venv $UV_VENV && \
    uv sync --frozen --no-dev

###############################################
# Development Image
###############################################
FROM builder-base AS development

# Install development dependencies
RUN uv sync --frozen

WORKDIR /app

###############################################
# Production Image
###############################################
FROM python-base AS production

# Copy virtual environment from builder
COPY --from=builder-base $UV_VENV $UV_VENV

# Copy application code
COPY ./app /app/app
COPY pyproject.toml /app/

WORKDIR /app

CMD ["python", "app/main.py"]