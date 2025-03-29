from typing import Literal

from pydantic import BaseModel, Field


class InviteLinkDto(BaseModel):
    link: str | None
    creator_id: int | None
    creator_username: str | None
    creator_first_name: str | None
    creator_last_name: str | None
    creator_is_bot: bool | None
    creator_is_premium: bool | None


class NewActionDto(BaseModel):
    telegram_id: int
    username: str | None
    is_bot: bool
    first_name: str | None
    last_name: str | None
    is_premium: bool | None
    link: InviteLinkDto | None
    action: Literal["enter", "leave"]
    channel_id: int
