from datetime import datetime, timezone

from app import db


class Usuario(db.Model):
    """Representa um usuário do sistema."""

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
    )

    senha_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    perfil = db.Column(
        db.String(20),
        nullable=False,
        default="COMUM",
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