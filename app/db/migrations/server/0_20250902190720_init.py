from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(64) NOT NULL UNIQUE,
    "email" VARCHAR(320) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL
);
COMMENT ON TABLE "user" IS 'Represent User in db.';
CREATE TABLE IF NOT EXISTS "resume" (
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(120) NOT NULL,
    "content" TEXT NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "resume" IS 'Represent Resume in db.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
