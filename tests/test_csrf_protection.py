import re

import pytest

from app.models.movimentacao import Movimentacao
from app.models.produto import Produto
from app.services.produto_service import criar_produto
from app.services.usuario_service import criar_usuario


def obter_token_csrf(client, path="/login"):
    resposta = client.get(path)
    assert resposta.status_code == 200

    match = re.search(
        r'name="csrf_token"[^>]*value="([^"]+)"',
        resposta.get_data(as_text=True),
    )
    assert match is not None

    return match.group(1)


def criar_usuario_teste(app, perfil, username=None):
    username = username or f"usuario_{perfil.lower()}"
    with app.app_context():
        return criar_usuario(
            nome=f"Usuário {perfil}",
            username=username,
            senha="senha-de-teste",
            perfil=perfil,
        )


def autenticar(client, username="usuario_admin"):
    token = obter_token_csrf(client)
    return client.post(
        "/login",
        data={
            "csrf_token": token,
            "username": username,
            "senha": "senha-de-teste",
        },
    )


def test_post_sem_token_csrf_e_rejeitado(client):
    resposta = client.post(
        "/login",
        data={"username": "qualquer", "senha": "qualquer"},
    )

    assert resposta.status_code == 400


def test_login_com_token_csrf_invalido_e_rejeitado(app, client):
    criar_usuario_teste(app, "ADMIN")

    resposta = client.post(
        "/login",
        data={
            "csrf_token": "token-invalido",
            "username": "usuario_admin",
            "senha": "senha-de-teste",
        },
    )

    assert resposta.status_code == 400


def test_post_com_token_csrf_invalido_e_rejeitado(app, client):
    criar_usuario_teste(app, "ADMIN")
    assert autenticar(client).status_code == 302

    resposta = client.post(
        "/produtos/novo",
        data={
            "csrf_token": "token-invalido",
            "codigo": "PROD-CSRF",
            "nome": "Produto CSRF",
            "quantidade_inicial": "0",
            "estoque_minimo": "0",
            "preco": "1.00",
        },
    )

    assert resposta.status_code == 400


def test_login_com_token_csrf_valido_continua_funcionando(app, client):
    criar_usuario_teste(app, "ADMIN")
    token = obter_token_csrf(client)

    resposta = client.post(
        "/login",
        data={
            "csrf_token": token,
            "username": "usuario_admin",
            "senha": "senha-de-teste",
        },
    )

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/")
    assert client.get("/").status_code == 200


def test_post_autorizado_com_token_csrf_valido_e_aceito(app, client):
    criar_usuario_teste(app, "ADMIN")
    assert autenticar(client).status_code == 302
    token = obter_token_csrf(client, "/produtos/novo")

    resposta = client.post(
        "/produtos/novo",
        data={
            "csrf_token": token,
            "codigo": "PROD-CSRF",
            "nome": "Produto CSRF",
            "quantidade_inicial": "0",
            "estoque_minimo": "0",
            "preco": "1.00",
        },
    )

    assert resposta.status_code == 302
    with app.app_context():
        assert Produto.query.filter_by(codigo="PROD-CSRF").first()


def test_operacao_administrativa_continua_restrita_a_admin(app, client):
    criar_usuario_teste(app, "COMUM")
    assert autenticar(client, "usuario_comum").status_code == 302
    token = obter_token_csrf(client, "/produtos")

    resposta = client.post(
        "/produtos/novo",
        data={
            "csrf_token": token,
            "codigo": "PROD-NEGADO",
            "nome": "Produto sem permissão",
            "quantidade_inicial": "0",
            "estoque_minimo": "0",
            "preco": "1.00",
        },
    )

    assert resposta.status_code == 403


@pytest.mark.parametrize("perfil", ["ADMIN", "COMUM"])
def test_admin_e_comum_podem_criar_movimentacao_com_token(app, client, perfil):
    username = f"usuario_{perfil.lower()}"
    criar_usuario_teste(app, perfil, username)
    with app.app_context():
        criar_produto(
            codigo="PROD-MOV-CSRF",
            nome="Produto para movimentação",
            descricao="",
            categoria="",
            quantidade_inicial=2,
            estoque_minimo=0,
            preco=1,
        )

    assert autenticar(client, username).status_code == 302
    token = obter_token_csrf(client, "/")

    resposta = client.post(
        "/movimentacoes/nova",
        data={
            "csrf_token": token,
            "produto_id": "1",
            "tipo": "ENTRADA",
            "quantidade": "1",
            "observacao": "Teste CSRF",
        },
    )

    assert resposta.status_code == 302
    with app.app_context():
        assert Movimentacao.query.count() == 1
        assert Produto.query.filter_by(
            codigo="PROD-MOV-CSRF"
        ).one().quantidade_atual == 3


def test_demo_continua_sem_permissao_de_escrita_com_token(app, client):
    criar_usuario_teste(app, "DEMO")
    with app.app_context():
        criar_produto(
            codigo="PROD-DEMO-CSRF",
            nome="Produto para DEMO",
            descricao="",
            categoria="",
            quantidade_inicial=2,
            estoque_minimo=0,
            preco=1,
        )

    assert autenticar(client, "usuario_demo").status_code == 302
    token = obter_token_csrf(client, "/")

    resposta = client.post(
        "/movimentacoes/nova",
        data={
            "csrf_token": token,
            "produto_id": "1",
            "tipo": "ENTRADA",
            "quantidade": "1",
        },
    )

    assert resposta.status_code == 403
    with app.app_context():
        assert Movimentacao.query.count() == 0
        assert Produto.query.filter_by(
            codigo="PROD-DEMO-CSRF"
        ).one().quantidade_atual == 2


def test_logout_exige_post_com_token_csrf_e_preserva_redirecionamento(app, client):
    criar_usuario_teste(app, "ADMIN")
    assert autenticar(client).status_code == 302
    token = obter_token_csrf(client, "/")

    assert client.get("/logout").status_code == 405

    resposta = client.post(
        "/logout",
        data={"csrf_token": token},
    )

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/login")
    assert client.get("/").status_code == 302


def test_paginas_get_de_leitura_continuam_disponiveis_para_demo(app, client):
    criar_usuario_teste(app, "DEMO")
    assert autenticar(client, "usuario_demo").status_code == 302

    for path in ("/", "/produtos", "/movimentacoes"):
        assert client.get(path).status_code == 200
