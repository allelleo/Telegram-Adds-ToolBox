# Telegram tool for addss

## Main Branches:
- main -> Prod
- testing -> main
- stable -> testing
- dev -> stable


## Aerich && Работа с базой данных и миграциями
### Инициализция `aerich`
```commandline
poetry run aerich init -t src.telegram_add_tool.backend.src.core.database.TORTOISE_CONFIG
poetry run aerich init-db
```
### Создание миграции
```commandline
poetry run aerich migrate --name add_password_to_user
```
### Применение миграции / откат миграции
```commandline
poetry run aerich upgrade
poetry run aerich downgrade
```
### История миграций
```commandline
poetry run aerich history
poetry run aerich heads
```


### Запуск
```commandline
poetry sync
```
#### Backend
```commandline
uvicorn src.telegram_add_tool.backend.app:app
```

#### Bot
```commandline
poetry run python3.12 bot.py
```

#### Avatars
```commandline
poetry run python3.12 src/telegram_add_tool/user_avatar_date_module/app.py
```

#### RegDate
```commandline
poetry run python3.12 src/telegram_add_tool/user_created_account/app.py
```

#### UsStatus
```commandline
poetry run python3.12 src/telegram_add_tool/activity_checker/app.py
```

## Bot commands
- `/panel` Основная панель
- `/channel {channel_id}` - Информация по каналу
- `/channel_users {channel_id}` - Информация обо всех юзерах которых отследили в канале
- `/link {link_id}` - Информация по юзерам которые пришли по ссылке
- `/link_t {raw_link}` - Информация по юзерам которые перешли по ссылке