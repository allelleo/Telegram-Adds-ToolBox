# manage.py
from dotenv import load_dotenv

load_dotenv()

import typer
import subprocess

cli = typer.Typer()


@cli.command()
def make_migrations(name: str):
    """Создать новую миграцию."""
    subprocess.run(["poetry", "run", "aerich", "migrate", "--name", name])


@cli.command()
def migrate():
    """Применить миграции."""
    subprocess.run(["poetry", "run", "aerich", "upgrade"])


@cli.command()
def downgrade():
    """Откатить последнюю миграцию."""
    subprocess.run(["poetry", "run", "aerich", "downgrade"])


@cli.command()
def history():
    """Показать историю миграций."""
    subprocess.run(["poetry", "run", "aerich", "history"])


@cli.command()
def heads():
    """Показать актуальные миграции."""
    subprocess.run(["poetry", "run", "aerich", "heads"])


@cli.command()
def init_db():
    """Инициализировать базу данных."""
    subprocess.run(["poetry", "run", "aerich", "init-db"])


if __name__ == "__main__":
    cli()
