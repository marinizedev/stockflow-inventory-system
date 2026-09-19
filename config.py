import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def obter_database_url():
    """
    Retorna a URL do banco definida no ambiente.

    Sem DATABASE_URL, a aplicação utiliza SQLite localmente.
    Com DATABASE_URL, utiliza PostgreSQL ou outro banco configurado.
    """

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        return (
            f"sqlite:///{BASE_DIR / 'database' / 'stockflow.db'}"
        )

    if database_url.startswith("postgres://"):
        return database_url.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )

    if database_url.startswith("postgresql://"):
        return database_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    return database_url


class Config:
    """Configurações base da aplicação."""

    SECRET_KEY = os.getenv(
        "STOCKFLOW_SECRET_KEY",
        "chave-local-do-stockflow",
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO",
    ).upper()

    SQLALCHEMY_DATABASE_URI = obter_database_url()

    SQLALCHEMY_TRACK_MODIFICATIONS = False
