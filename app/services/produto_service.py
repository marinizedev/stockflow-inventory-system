from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.produto import Produto


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
        raise

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
        raise

def inativar_produto(produto):
    """Inativa um produto sem remover seu histórico."""

    if not produto.ativo:
        return

    produto.ativo = False

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise


def ativar_produto(produto):
    """Ativa novamente um produto."""

    if produto.ativo:
        return

    produto.ativo = True

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        raise