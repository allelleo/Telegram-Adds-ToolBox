from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "userorm_userphotoorm";
        ALTER TABLE "userorm" ADD "photo_date" TIMESTAMPTZ;
        DROP TABLE IF EXISTS "userphotoorm";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "userorm" DROP COLUMN "photo_date";
        CREATE TABLE "userorm_userphotoorm" (
    "userorm_id" INT NOT NULL REFERENCES "userorm" ("id") ON DELETE CASCADE,
    "userphotoorm_id" INT NOT NULL REFERENCES "userphotoorm" ("id") ON DELETE CASCADE
);"""
