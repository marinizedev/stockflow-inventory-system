from datetime import datetime, timezone
from decimal import Decimal

from app import db


class Produto(db.Model):
    """Representa um produto controlado pelo estoque."""

    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)

    codigo = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
    )

    nome = db.Column(
        db.String(100),
        nullable=False,
    )

    descricao = db.Column(
        db.Text,
        nullable=True,
    )

    categoria = db.Column(
        db.String(50),
        nullable=True,
    )

    quantidade_atual = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    estoque_minimo = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    preco = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    ativo = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )