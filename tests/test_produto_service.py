from decimal import Decimal

import pytest

from app.services.produto_service import (
    criar_produto,
    editar_produto,
    inativar_produto,
    ativar_produto,
)


def test_criar_produto_com_dados_validos(app):
    produto = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="Sabão em pó 2.4kg",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    assert produto.id is not None
    assert produto.codigo == "PROD-001"
    assert produto.nome == "Sabão em Pó"
    assert produto.descricao == "Sabão em pó 2.4kg"
    assert produto.categoria == "Limpeza"
    assert produto.quantidade_atual == 10
    assert produto.estoque_minimo == 3
    assert produto.preco == Decimal("25.90")
    assert produto.ativo is True


def test_criar_produto_exige_codigo(app):
    with pytest.raises(
        ValueError,
        match="O código é obrigatório.",
    ):
        criar_produto(
            codigo="",
            nome="Sabão em Pó",
            descricao="",
            categoria="Limpeza",
            quantidade_inicial=10,
            estoque_minimo=3,
            preco=25.90,
        )


def test_criar_produto_exige_nome(app):
    with pytest.raises(
        ValueError,
        match="O nome é obrigatório.",
    ):
        criar_produto(
            codigo="PROD-001",
            nome="",
            descricao="",
            categoria="Limpeza",
            quantidade_inicial=10,
            estoque_minimo=3,
            preco=25.90,
        )


def test_criar_produto_rejeita_codigo_duplicado(app):
    criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    with pytest.raises(
        ValueError,
        match="Esse código já está cadastrado.",
    ):
        criar_produto(
            codigo="PROD-001",
            nome="Detergente",
            descricao="",
            categoria="Limpeza",
            quantidade_inicial=5,
            estoque_minimo=2,
            preco=4.50,
        )


def test_criar_produto_rejeita_quantidade_inicial_negativa(app):
    with pytest.raises(
        ValueError,
        match="A quantidade inicial não pode ser negativa.",
    ):
        criar_produto(
            codigo="PROD-001",
            nome="Sabão em Pó",
            descricao="",
            categoria="Limpeza",
            quantidade_inicial=-1,
            estoque_minimo=3,
            preco=25.90,
        )


def test_criar_produto_rejeita_estoque_minimo_negativo(app):
    with pytest.raises(
        ValueError,
        match="O estoque mínimo não pode ser negativo.",
    ):
        criar_produto(
            codigo="PROD-001",
            nome="Sabão em Pó",
            descricao="",
            categoria="Limpeza",
            quantidade_inicial=10,
            estoque_minimo=-1,
            preco=25.90,
        )


def test_criar_produto_rejeita_preco_negativo(app):
    with pytest.raises(
        ValueError,
        match="O preço não pode ser negativo.",
    ):
        criar_produto(
            codigo="PROD-001",
            nome="Sabão em Pó",
            descricao="",
            categoria="Limpeza",
            quantidade_inicial=10,
            estoque_minimo=3,
            preco=-25.90,
        )


def test_criar_produto_permite_descricao_e_categoria_vazias(app):
    produto = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="",
        categoria="",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    assert produto.descricao is None
    assert produto.categoria is None


def test_editar_produto_com_dados_validos(app):
    produto = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="Descrição antiga",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    editar_produto(
        produto,
        codigo="PROD-002",
        nome="Sabão em Pó Premium",
        descricao="Descrição nova",
        categoria="Higiene",
        estoque_minimo=5,
        preco=29.90,
    )

    assert produto.codigo == "PROD-002"
    assert produto.nome == "Sabão em Pó Premium"
    assert produto.descricao == "Descrição nova"
    assert produto.categoria == "Higiene"
    assert produto.estoque_minimo == 5
    assert produto.preco == Decimal("29.90")


def test_editar_produto_nao_altera_estoque_atual(app):
    produto = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    editar_produto(
        produto,
        codigo="PROD-001",
        nome="Sabão em Pó Atualizado",
        descricao="",
        categoria="Limpeza",
        estoque_minimo=5,
        preco=27.90,
    )

    assert produto.quantidade_atual == 10


def test_editar_produto_rejeita_codigo_duplicado(app):
    primeiro = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    criar_produto(
        codigo="PROD-002",
        nome="Detergente",
        descricao="",
        categoria="Limpeza",
        quantidade_inicial=5,
        estoque_minimo=2,
        preco=4.50,
    )

    with pytest.raises(
        ValueError,
        match="Esse código já está cadastrado.",
    ):
        editar_produto(
            primeiro,
            codigo="PROD-002",
            nome="Sabão em Pó",
            descricao="",
            categoria="Limpeza",
            estoque_minimo=3,
            preco=25.90,
        )


def test_editar_produto_rejeita_estoque_minimo_negativo(app):
    produto = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    with pytest.raises(
        ValueError,
        match="O estoque mínimo não pode ser negativo.",
    ):
        editar_produto(
            produto,
            codigo="PROD-001",
            nome="Sabão em Pó",
            descricao="",
            categoria="Limpeza",
            estoque_minimo=-1,
            preco=25.90,
        )


def test_editar_produto_rejeita_preco_negativo(app):
    produto = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    with pytest.raises(
        ValueError,
        match="O preço não pode ser negativo.",
    ):
        editar_produto(
            produto,
            codigo="PROD-001",
            nome="Sabão em Pó",
            descricao="",
            categoria="Limpeza",
            estoque_minimo=3,
            preco=-10,
        )


def test_inativar_produto(app):
    produto = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    inativar_produto(produto)

    assert produto.ativo is False


def test_ativar_produto(app):
    produto = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    inativar_produto(produto)

    assert produto.ativo is False

    ativar_produto(produto)

    assert produto.ativo is True