import logging
import os
import sys


def configurar_logging():
    """Configura o logging principal da aplicação."""

    nivel_configurado = os.getenv(
        "LOG_LEVEL",
        "INFO",
    ).upper()

    nivel = getattr(
        logging,
        nivel_configurado,
        logging.INFO,
    )

    logging.basicConfig(
        level=nivel,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )
