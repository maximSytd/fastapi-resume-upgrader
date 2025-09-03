FROM python:3.11-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    USE_DOCKER=1 \
    LANG=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8 \
    LC_TIME=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$VENV_PATH/bin:$PATH"

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
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR $PYSETUP_PATH
COPY pyproject.toml uv.lock ./

RUN uv venv $VENV_PATH && \
    uv sync --frozen --no-dev

###############################################
# Development Image
###############################################
FROM builder-base AS development
RUN uv sync --frozen
WORKDIR /app/

###############################################
# Production Image
###############################################
FROM python-base AS production

# Copy virtual environment from builder
COPY --from=builder-base $VENV_PATH $VENV_PATH

# Copy ONLY the app folder (which contains config inside)
COPY ./app /app/

WORKDIR /app/
CMD ["python", "main.py"]