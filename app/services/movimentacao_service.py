import logging

from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.movimentacao import Movimentacao
from app.models.produto import Produto
from app.models.usuario import Usuario


logger = logging.getLogger(__name__)


def registrar_movimentacao(
    produto,
    usuario,
    tipo,
    quantidade,
    observacao=None,
):
    """Registra uma entrada ou saída de estoque."""

    if not isinstance(produto, Produto):
        logger.warning(
            "Tentativa de movimentação com produto inválido"
        )

        raise ValueError("Produto inválido.")

    if not isinstance(usuario, Usuario):
        logger.warning(
            "Tentativa de movimentação com usuário inválido"
        )

        raise ValueError("Usuário inválido.")

    if tipo not in {"ENTRADA", "SAIDA"}:
        logger.warning(
            "Tipo de movimentação inválido: tipo=%s",
            tipo,
        )

        raise ValueError("Tipo de movimentação inválido.")

    if quantidade <= 0:
        logger.warning(
            "Quantidade inválida em movimentação: "
            "quantidade=%s",
            quantidade,
        )

        raise ValueError(
            "A quantidade deve ser maior que zero."
        )

    if not produto.ativo:
        logger.warning(
            "Tentativa de movimentar produto inativo: "
            "produto_id=%s codigo=%s usuario_id=%s",
            produto.id,
            produto.codigo,
            usuario.id,
        )

        raise ValueError(
            "Não é possível movimentar um produto inativo."
        )

    if tipo == "SAIDA":
        if quantidade > produto.quantidade_atual:
            logger.warning(
                "Saída superior ao estoque disponível: "
                "produto_id=%s estoque_atual=%s "
                "quantidade_solicitada=%s usuario_id=%s",
                produto.id,
                produto.quantidade_atual,
                quantidade,
                usuario.id,
            )

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
        observacao=(
            observacao.strip()
            if observacao
            else None
        ),
    )

    db.session.add(movimentacao)

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        logger.exception(
            "Erro ao persistir movimentação: "
            "produto_id=%s usuario_id=%s tipo=%s "
            "quantidade=%s",
            produto.id,
            usuario.id,
            tipo,
            quantidade,
        )

        raise

    logger.info(
        "Movimentação registrada com sucesso: "
        "movimentacao_id=%s produto_id=%s codigo=%s "
        "usuario_id=%s tipo=%s quantidade=%s "
        "estoque_atual=%s",
        movimentacao.id,
        produto.id,
        produto.codigo,
        usuario.id,
        tipo,
        quantidade,
        produto.quantidade_atual,
    )

    return movimentacao
