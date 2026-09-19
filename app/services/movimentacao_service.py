from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.movimentacao import Movimentacao
from app.models.produto import Produto
from app.models.usuario import Usuario


def registrar_movimentacao(
    produto,
    usuario,
    tipo,
    quantidade,
    observacao=None,
):
    """Registra uma entrada ou saída de estoque."""

    if not isinstance(produto, Produto):
        raise ValueError("Produto inválido.")

    if not isinstance(usuario, Usuario):
        raise ValueError("Usuário inválido.")

    if tipo not in {"ENTRADA", "SAIDA"}:
        raise ValueError("Tipo de movimentação inválido.")

    if quantidade <= 0:
        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    if not produto.ativo:
        raise ValueError(
            "Não é possível movimentar um produto inativo."
        )

    if tipo == "SAIDA":
        if quantidade > produto.quantidade_atual:
            raise ValueError(
                "A saída não pode deixar o estoque negativo."
            )

        produto.quantidade_atual -= quantidade

    else:
        produto.quantidade_atual += quantidade

    movimentacao = Movimentacao(
        produto_id=produto.id,
        usuario_id=usuario.id,
        tipo=tipo,
        quantidade=quantidade,
        observacao=observacao.strip() if observacao else None,
    )

    db.session.add(movimentacao)

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise

    return movimentacao