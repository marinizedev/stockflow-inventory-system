from datetime import datetime, timezone

from app import db


class Movimentacao(db.Model):
    """Representa uma entrada ou saída de estoque."""

    __tablename__ = "movimentacoes"

    id = db.Column(db.Integer, primary_key=True)

    produto_id = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id"),
        nullable=False,
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False,
    )

    tipo = db.Column(
        db.String(10),
        nullable=False,
    )

    quantidade = db.Column(
        db.Integer,
        nullable=False,
    )

    observacao = db.Column(
        db.Text,
        nullable=True,
    )

    realizado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    produto = db.relationship(
        "Produto",
        backref="movimentacoes",
    )

    usuario = db.relationship(
        "Usuario",
        backref="movimentacoes",
    )