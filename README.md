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
