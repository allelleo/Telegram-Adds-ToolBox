from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "channelsorm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "version" INT NOT NULL DEFAULT 1,
    "title" VARCHAR(255) NOT NULL,
    "channel_id" BIGINT NOT NULL
);
CREATE TABLE IF NOT EXISTS "invitelinksorm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "version" INT NOT NULL DEFAULT 1,
    "link" VARCHAR(255) NOT NULL,
    "creator_id" BIGINT NOT NULL,
    "creator_username" VARCHAR(255),
    "creator_first_name" VARCHAR(255),
    "creator_last_name" VARCHAR(255),
    "creator_is_bot" BOOL NOT NULL DEFAULT False,
    "creator_is_premium" BOOL NOT NULL DEFAULT False,
    "channel_id" INT NOT NULL REFERENCES "channelsorm" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "useractivitystatusorm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "version" INT NOT NULL DEFAULT 1,
    "status" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "userorm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "version" INT NOT NULL DEFAULT 1,
    "telegram_id" BIGINT NOT NULL,
    "username" VARCHAR(255),
    "is_bot" BOOL NOT NULL DEFAULT False,
    "first_name" VARCHAR(255),
    "last_name" VARCHAR(255),
    "is_premium" BOOL NOT NULL DEFAULT False
);
CREATE TABLE IF NOT EXISTS "useractionhistoryorm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "version" INT NOT NULL DEFAULT 1,
    "action" VARCHAR(255) NOT NULL,
    "channel_id" INT NOT NULL REFERENCES "channelsorm" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "userorm" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "userphotoorm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "version" INT NOT NULL DEFAULT 1,
    "path" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "userorm_userphotoorm" (
    "userorm_id" INT NOT NULL REFERENCES "userorm" ("id") ON DELETE CASCADE,
    "userphotoorm_id" INT NOT NULL REFERENCES "userphotoorm" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_userorm_use_userorm_1d7e4c" ON "userorm_userphotoorm" ("userorm_id", "userphotoorm_id");
CREATE TABLE IF NOT EXISTS "userorm_invitelinksorm" (
    "userorm_id" INT NOT NULL REFERENCES "userorm" ("id") ON DELETE CASCADE,
    "invitelinksorm_id" INT NOT NULL REFERENCES "invitelinksorm" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_userorm_inv_userorm_d3033b" ON "userorm_invitelinksorm" ("userorm_id", "invitelinksorm_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
