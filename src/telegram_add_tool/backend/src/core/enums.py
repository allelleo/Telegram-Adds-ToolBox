# src/oauth/core/enums.py

from enum import IntEnum


class UserPlatformEnum(IntEnum):
    WEB = 0
    ANDROID = 1
    IOS = 2


class AuthClientIdEnum(IntEnum):
    HALFCODER = 0
