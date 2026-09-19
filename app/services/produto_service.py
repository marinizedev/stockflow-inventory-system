import logging

from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.produto import Produto


logger = logging.getLogger(__name__)


def criar_produto(
    codigo,
    nome,
    descricao,
    categoria,
    quantidade_inicial,
    estoque_minimo,
    preco,
):
    """Cria um produto respeitando as regras de negócio."""

    codigo = codigo.strip()
    nome = nome.strip()
    descricao = descricao.strip()
    categoria = categoria.strip()

    if not codigo:
        raise ValueError("O código é obrigatório.")

    if not nome:
        raise ValueError("O nome é obrigatório.")

    produto_existente = Produto.query.filter_by(
        codigo=codigo
    ).first()

    if produto_existente:
        raise ValueError(
            "Esse código já está cadastrado."
        )

    if quantidade_inicial < 0:
        raise ValueError(
            "A quantidade inicial não pode ser negativa."
        )

    if estoque_minimo < 0:
        raise ValueError(
            "O estoque mínimo não pode ser negativo."
        )

    if preco < 0:
        raise ValueError(
            "O preço não pode ser negativo."
        )

    produto = Produto(
        codigo=codigo,
        nome=nome,
        descricao=descricao or None,
        categoria=categoria or None,
        quantidade_atual=quantidade_inicial,
        estoque_minimo=estoque_minimo,
        preco=preco,
        ativo=True,
    )

    db.session.add(produto)

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        logger.exception(
            "Erro ao criar produto: codigo=%s nome=%s",
            codigo,
            nome,
        )

        raise

    logger.info(
        "Produto criado com sucesso: "
        "produto_id=%s codigo=%s nome=%s "
        "quantidade_inicial=%s",
        produto.id,
        produto.codigo,
        produto.nome,
        produto.quantidade_atual,
    )

    return produto


def editar_produto(
    produto,
    codigo,
    nome,
    descricao,
    categoria,
    estoque_minimo,
    preco,
):
    """Edita os dados de um produto sem alterar o estoque atual."""

    codigo = codigo.strip()
    nome = nome.strip()
    descricao = descricao.strip()
    categoria = categoria.strip()

    if not codigo:
        raise ValueError("O código é obrigatório.")

    if not nome:
        raise ValueError("O nome é obrigatório.")

    produto_existente = Produto.query.filter(
        Produto.codigo == codigo,
        Produto.id != produto.id,
    ).first()

    if produto_existente:
        raise ValueError(
            "Esse código já está cadastrado."
        )

    if estoque_minimo < 0:
        raise ValueError(
            "O estoque mínimo não pode ser negativo."
        )

    if preco < 0:
        raise ValueError(
            "O preço não pode ser negativo."
        )

    produto.codigo = codigo
    produto.nome = nome
    produto.descricao = descricao or None
    produto.categoria = categoria or None
    produto.estoque_minimo = estoque_minimo
    produto.preco = preco

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        logger.exception(
            "Erro ao editar produto: produto_id=%s",
            produto.id,
        )

        raise

    logger.info(
        "Produto editado com sucesso: "
        "produto_id=%s codigo=%s nome=%s",
        produto.id,
        produto.codigo,
        produto.nome,
    )


def inativar_produto(produto):
    """Inativa um produto sem remover seu histórico."""

    if not produto.ativo:
        logger.info(
            "Produto já estava inativo: "
            "produto_id=%s codigo=%s",
            produto.id,
            produto.codigo,
        )

        return

    produto.ativo = False

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        logger.exception(
            "Erro ao inativar produto: "
            "produto_id=%s codigo=%s",
            produto.id,
            produto.codigo,
        )

        raise

    logger.info(
        "Produto inativado com sucesso: "
        "produto_id=%s codigo=%s",
        produto.id,
        produto.codigo,
    )


def ativar_produto(produto):
    """Ativa novamente um produto."""

    if produto.ativo:
        logger.info(
            "Produto já estava ativo: "
            "produto_id=%s codigo=%s",
            produto.id,
            produto.codigo,
        )

        return

    produto.ativo = True

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        logger.exception(
            "Erro ao ativar produto: "
            "produto_id=%s codigo=%s",
            produto.id,
            produto.codigo,
        )

        raise

    logger.info(
        "Produto ativado com sucesso: "
        "produto_id=%s codigo=%s",
        produto.id,
        produto.codigo,
    )
