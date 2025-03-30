from datetime import datetime, timedelta, timezone
from collections import defaultdict
import re
import dateparser

from src.telegram_add_tool.backend.src.apps.user.models import (
    InviteLinksOrm,
    UserOrm,
    UserActionHistoryOrm,
    UserActivityStatusOrm,
)


async def get_users_with_link_and_enter_action(link_id) -> list[UserOrm]:
    # Получаем ссылку с id=6 и канал, к которому она привязана
    link = await InviteLinksOrm.get(id=link_id).prefetch_related("channel")
    channel = link.channel

    # Пользователи, использовавшие эту ссылку
    users = await UserOrm.filter(used_links__id=link_id).prefetch_related("used_links")

    result_users = []

    for user in users:
        # Последнее действие пользователя в этом канале
        last_action = (
            await UserActionHistoryOrm.filter(user=user, channel=channel)
            .order_by("-id")
            .first()
        )

        if last_action and last_action.action == "enter":
            result_users.append(user)

    return result_users


def parse_registration_date(message: str) -> datetime | None:
    match = re.search(r"Estimated registration date: (.+)", message or "")
    return dateparser.parse(match.group(1)) if match else None


def categorize_date(date: datetime | None, now: datetime) -> str:
    if date is None:
        return "отсутствует"

    if date.tzinfo is not None:
        date = date.astimezone(timezone.utc).replace(tzinfo=None)

    delta = now.replace(tzinfo=None) - date
    if delta.days == 0:
        return "день"
    elif delta.days <= 7:
        return "до недели"
    elif delta.days <= 30:
        return "до месяца"
    elif delta.days <= 90:
        return "до 3-х месяцев"
    elif delta.days <= 180:
        return "до полугода"
    elif delta.days <= 1095:
        return "Больше года"
    else:
        return "Больше 3-ех лет"


async def get_user_metrics(users: list[UserOrm]) -> dict:
    now = datetime.now(timezone.utc)
    total = len(users)
    is_prem = sum(1 for user in users if user.is_premium)

    # Шаблоны
    activity_map = defaultdict(list)
    reg_map = defaultdict(list)
    avatar_map = defaultdict(list)

    for user in users:
        # 📍 Activity
        last_status = (
            await UserActivityStatusOrm.filter(user=user).order_by("-timestamp").first()
        )
        if not last_status:
            activity_map["недавно"].append(user)
        else:
            delta = now - last_status.timestamp
            if timedelta(hours=6) <= delta <= timedelta(hours=12):
                activity_map["6-12 часов назад"].append(user)
            elif timedelta(hours=13) <= delta <= timedelta(hours=24):
                activity_map["13-24 часа назад"].append(user)
            elif (now - timedelta(days=7)) <= last_status.timestamp:
                activity_map["на этой неделе"].append(user)
            elif (now - timedelta(days=30)) <= last_status.timestamp:
                activity_map["в этом месяце"].append(user)
            else:
                activity_map["давно"].append(user)

        # 📍 Registration
        reg_date = parse_registration_date(user.registration_message)
        reg_cat = categorize_date(reg_date, now)
        reg_map[reg_cat].append(user)

        # 📍 Avatar Date
        avatar_cat = categorize_date(user.photo_date, now)
        avatar_map[avatar_cat].append(user)

    def build_metrics(
        counter: dict[str, list], categories: list[str]
    ) -> dict[str, str]:
        result = {}
        for category in categories:
            count = len(counter.get(category, []))
            percent = round((count / total) * 100, 1) if total else 0.0
            result[category] = f"{count} ({percent}%)"
        return result

    activity_categories = [
        "недавно",
        "6-12 часов назад",
        "13-24 часа назад",
        "на этой неделе",
        "в этом месяце",
        "давно",
    ]

    time_categories = [
        "отсутствует",
        "день",
        "до недели",
        "до месяца",
        "до 3-х месяцев",
        "до полугода",
        "Больше года",
        "Больше 3-ех лет",
    ]

    return {
        "Были в сети": build_metrics(activity_map, activity_categories),
        "Дата регистрации": build_metrics(reg_map, time_categories),
        "Дата постановки аватарки": build_metrics(avatar_map, time_categories),
        "total": total,
        "is_prem": is_prem,
    }
