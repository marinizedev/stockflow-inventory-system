import pytest

from app import create_app, db
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.movimentacao import Movimentacao
from config import Config


@pytest.fixture
def app(monkeypatch):
    """Cria uma aplicação isolada para os testes."""

    monkeypatch.setattr(
        Config,
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///:memory:",
    )

    app = create_app()

    app.config.update(
        TESTING=True,
        SECRET_KEY="chave-de-teste",
    )

    with app.app_context():
        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Cria um cliente HTTP para testes de rotas."""

    return app.test_client()