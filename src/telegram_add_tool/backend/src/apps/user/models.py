from src.telegram_add_tool.backend.src.core.abstract_orm_model import (
    BaseAbstractOrmModel,
)

from tortoise import fields

class BotUserAccessOrm(BaseAbstractOrmModel):
    telegram_id: int = fields.BigIntField()
    name: str = fields.CharField(max_length=255)

class ChannelsOrm(BaseAbstractOrmModel):
    title: str = fields.CharField(max_length=255)
    channel_id: int = fields.BigIntField()


class UserActivityStatusOrm(BaseAbstractOrmModel):
    status: str = fields.CharField(max_length=255)


class InviteLinksOrm(BaseAbstractOrmModel):
    link: str = fields.CharField(max_length=255)
    creator_id: int = fields.BigIntField()
    creator_username: str = fields.CharField(max_length=255, null=True)
    creator_first_name: str = fields.CharField(max_length=255, null=True)
    creator_last_name: str = fields.CharField(max_length=255, null=True)
    creator_is_bot: bool = fields.BooleanField(default=False)
    creator_is_premium: bool = fields.BooleanField(default=False)
    channel = fields.ForeignKeyField("models.ChannelsOrm")


class UserActionHistoryOrm(BaseAbstractOrmModel):
    action: str = fields.CharField(max_length=255)
    channel = fields.ForeignKeyField("models.ChannelsOrm")
    user = fields.ForeignKeyField("models.UserOrm")


class UserOrm(BaseAbstractOrmModel):
    telegram_id: int = fields.BigIntField()
    username: str = fields.CharField(max_length=255, null=True)
    is_bot: bool = fields.BooleanField(default=False)
    first_name: str = fields.CharField(max_length=255, null=True)
    last_name: str = fields.CharField(max_length=255, null=True)
    is_premium: bool = fields.BooleanField(default=False)
    used_links = fields.ManyToManyField("models.InviteLinksOrm", related_name="users")
    photo_date = fields.DatetimeField(null=True)
    registration_message = fields.CharField(max_length=500, null=True)
    registration_date = fields.CharField(max_length=500, null=True)
