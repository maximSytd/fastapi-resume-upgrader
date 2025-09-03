# FastAPI Docker Boilerplate

This project is based on [FastAPI Docker Boilerplate](https://github.com/Afaneor/fastapi-docker-boilerplate).

## Table of Contents

- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [CI/CD](#cicd)

## Setup

### ✅ Prerequisites

- [Python](https://www.python.org/) (3.11+ recommended)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

1. Clone the repository
   ```
   git clone https://github.com/maximSytd/fastapi-resume-upgrader.git &&
   cd fastapi-resume-upgrader && uv sync --active
   ```
2. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```
3. Configure the environment variables in the `.env` file

## Running the Application

### Locally

```shell
python3 app/main.py
```

### Using Docker

```shell
docker-compose up -d
```

### using docker for development

```shell
docker-compose -f docker-compose.local.yml up -d
```

## Configuration

Project settings are divided into components and environments (development/production). They are located in the `app/config/components/` directory.

The main logic for combining settings is in the `__init__.py` file.

To switch between environments, change the `ENVIRONMENT` variable in the `.env` file.

##  Migrations

The project uses [Tortoise ORM](https://github.com/tortoise/tortoise-orm) and [Aerich](https://github.com/tortoise/aerich) for managing migrations.

### Initializing Migrations

```shell
aerich init-db
```

This will create a migrations folder in the db module. All models in `__init__.py` (db module) will be reflected in the migration.

### Creating a New Migration

```shell
aerich migrate
```

### Applying Migrations

```shell
aerich upgrade
```

##  Swagger
[here](http://127.0.0.1:8000/docs#/)

##  Tests
```shell
pytest
```

## CI/CD

The project includes a basic CI/CD configuration using GitLab CI. The `.gitlab-ci.yml` file contains stage for building image of the application.