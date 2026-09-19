import pytest

from app.services.movimentacao_service import registrar_movimentacao
from app.services.produto_service import criar_produto
from app.services.usuario_service import criar_usuario


def criar_dados_base():
    """Cria usuário e produto para os testes de movimentação."""

    usuario = criar_usuario(
        nome="Marinize",
        username="marinize",
        senha="123456",
        perfil="ADMIN",
    )

    produto = criar_produto(
        codigo="PROD-001",
        nome="Sabão em Pó",
        descricao="",
        categoria="Limpeza",
        quantidade_inicial=10,
        estoque_minimo=3,
        preco=25.90,
    )

    return usuario, produto


def test_registrar_entrada_aumenta_estoque(app):
    usuario, produto = criar_dados_base()

    movimentacao = registrar_movimentacao(
        produto=produto,
        usuario=usuario,
        tipo="ENTRADA",
        quantidade=5,
    )

    assert produto.quantidade_atual == 15
    assert movimentacao.tipo == "ENTRADA"
    assert movimentacao.quantidade == 5


def test_registrar_saida_reduz_estoque(app):
    usuario, produto = criar_dados_base()

    movimentacao = registrar_movimentacao(
        produto=produto,
        usuario=usuario,
        tipo="SAIDA",
        quantidade=4,
    )

    assert produto.quantidade_atual == 6
    assert movimentacao.tipo == "SAIDA"
    assert movimentacao.quantidade == 4


def test_movimentacao_registra_produto_e_usuario(app):
    usuario, produto = criar_dados_base()

    movimentacao = registrar_movimentacao(
        produto=produto,
        usuario=usuario,
        tipo="ENTRADA",
        quantidade=5,
    )

    assert movimentacao.produto_id == produto.id
    assert movimentacao.usuario_id == usuario.id


def test_movimentacao_armazena_observacao(app):
    usuario, produto = criar_dados_base()

    movimentacao = registrar_movimentacao(
        produto=produto,
        usuario=usuario,
        tipo="ENTRADA",
        quantidade=5,
        observacao="Reposição mensal",
    )

    assert movimentacao.observacao == "Reposição mensal"


def test_movimentacao_sem_observacao_armazena_none(app):
    usuario, produto = criar_dados_base()

    movimentacao = registrar_movimentacao(
        produto=produto,
        usuario=usuario,
        tipo="ENTRADA",
        quantidade=5,
    )

    assert movimentacao.observacao is None


def test_saida_nao_pode_deixar_estoque_negativo(app):
    usuario, produto = criar_dados_base()

    with pytest.raises(
        ValueError,
        match="A saída não pode deixar o estoque negativo.",
    ):
        registrar_movimentacao(
            produto=produto,
            usuario=usuario,
            tipo="SAIDA",
            quantidade=11,
        )

    assert produto.quantidade_atual == 10


def test_rejeita_produto_invalido(app):
    usuario, _ = criar_dados_base()

    with pytest.raises(
        ValueError,
        match="Produto inválido.",
    ):
        registrar_movimentacao(
            produto="produto inválido",
            usuario=usuario,
            tipo="ENTRADA",
            quantidade=5,
        )


def test_rejeita_usuario_invalido(app):
    _, produto = criar_dados_base()

    with pytest.raises(
        ValueError,
        match="Usuário inválido.",
    ):
        registrar_movimentacao(
            produto=produto,
            usuario="usuario inválido",
            tipo="ENTRADA",
            quantidade=5,
        )


def test_rejeita_tipo_de_movimentacao_invalido(app):
    usuario, produto = criar_dados_base()

    with pytest.raises(
        ValueError,
        match="Tipo de movimentação inválido.",
    ):
        registrar_movimentacao(
            produto=produto,
            usuario=usuario,
            tipo="AJUSTE",
            quantidade=5,
        )


def test_rejeita_quantidade_zero(app):
    usuario, produto = criar_dados_base()

    with pytest.raises(
        ValueError,
        match="A quantidade deve ser maior que zero.",
    ):
        registrar_movimentacao(
            produto=produto,
            usuario=usuario,
            tipo="ENTRADA",
            quantidade=0,
        )


def test_rejeita_quantidade_negativa(app):
    usuario, produto = criar_dados_base()

    with pytest.raises(
        ValueError,
        match="A quantidade deve ser maior que zero.",
    ):
        registrar_movimentacao(
            produto=produto,
            usuario=usuario,
            tipo="ENTRADA",
            quantidade=-5,
        )


def test_nao_movimenta_produto_inativo(app):
    usuario, produto = criar_dados_base()

    produto.ativo = False

    with pytest.raises(
        ValueError,
        match="Não é possível movimentar um produto inativo.",
    ):
        registrar_movimentacao(
            produto=produto,
            usuario=usuario,
            tipo="ENTRADA",
            quantidade=5,
        )

    assert produto.quantidade_atual == 10