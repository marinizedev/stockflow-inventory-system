import logging

from sqlalchemy import update
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

    produto_id = produto.id
    produto_codigo = produto.codigo
    usuario_id = usuario.id

    try:
        condicoes = [
            Produto.id == produto_id,
            Produto.ativo.is_(True),
        ]

        if tipo == "SAIDA":
            condicoes.append(
                Produto.quantidade_atual >= quantidade
            )
            novo_saldo = Produto.quantidade_atual - quantidade
        else:
            novo_saldo = Produto.quantidade_atual + quantidade

        resultado = db.session.execute(
            update(Produto)
            .where(*condicoes)
            .values(quantidade_atual=novo_saldo),
            execution_options={"synchronize_session": False},
        )

        if resultado.rowcount != 1:
            db.session.refresh(
                produto,
                attribute_names=["ativo", "quantidade_atual"],
            )
            produto_ativo = produto.ativo
            estoque_atual = produto.quantidade_atual
            db.session.rollback()

            if not produto_ativo:
                logger.warning(
                    "Tentativa de movimentar produto inativo: "
                    "produto_id=%s codigo=%s usuario_id=%s",
                    produto_id,
                    produto_codigo,
                    usuario_id,
                )
                raise ValueError(
                    "Não é possível movimentar um produto inativo."
                )

            if tipo == "SAIDA":
                logger.warning(
                    "Saída superior ao estoque disponível: "
                    "produto_id=%s estoque_atual=%s "
                    "quantidade_solicitada=%s usuario_id=%s",
                    produto_id,
                    estoque_atual,
                    quantidade,
                    usuario_id,
                )
                raise ValueError(
                    "A saída não pode deixar o estoque negativo."
                )

            raise ValueError("Produto inválido.")

        db.session.refresh(
            produto,
            attribute_names=["quantidade_atual"],
        )

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
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        logger.exception(
            "Erro ao persistir movimentação: "
            "produto_id=%s usuario_id=%s tipo=%s "
            "quantidade=%s",
            produto_id,
            usuario_id,
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
        produto_id,
        produto_codigo,
        usuario_id,
        tipo,
        quantidade,
        produto.quantidade_atual,
    )

    return movimentacao
