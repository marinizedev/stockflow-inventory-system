import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Configurações base da aplicação."""

    SECRET_KEY = os.getenv(
        "STOCKFLOW_SECRET_KEY",
        "chave-local-do-stockflow",
    )

    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{BASE_DIR / 'database' / 'stockflow.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False