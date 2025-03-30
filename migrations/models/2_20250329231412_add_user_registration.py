from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "userorm" ADD "registration_date" VARCHAR(500);
        ALTER TABLE "userorm" ADD "registration_message" VARCHAR(500);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "userorm" DROP COLUMN "registration_date";
        ALTER TABLE "userorm" DROP COLUMN "registration_message";"""
