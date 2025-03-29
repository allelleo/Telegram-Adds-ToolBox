# src/oauth/core/abstract_orm_model.py

from datetime import datetime
from typing import Any

from tortoise import Model, fields
from tortoise.signals import pre_save


async def pre_save_model(
    sender: Any,
    instance: "BaseAbstractOrmModel",
    using_db: str,
    update_fields: list[str],
) -> None:
    instance.version += 1


class BaseAbstractOrmModel(Model):
    id: int = fields.IntField(pk=True)
    created_at: datetime = fields.DatetimeField(auto_now_add=True)
    updated_at: datetime = fields.DatetimeField(auto_now=True)
    is_deleted: bool = fields.BooleanField(default=False)
    version: int = fields.IntField(default=1)

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        pre_save(cls)(pre_save_model)

    class Meta:
        abstract = True
