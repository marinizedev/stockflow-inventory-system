from werkzeug.security import check_password_hash

import pytest

from app.services.usuario_service import (
    criar_usuario,
    pode_inativar_usuario,
    inativar_usuario,
    ativar_usuario,
    editar_usuario,
)


def test_criar_usuario_com_dados_validos(app):
    usuario = criar_usuario(
        nome="Marinize",
        username="marinize",
        senha="123456",
        perfil="ADMIN",
    )

    assert usuario.id is not None
    assert usuario.nome == "Marinize"
    assert usuario.username == "marinize"
    assert usuario.perfil == "ADMIN"
    assert usuario.ativo is True


def test_criar_usuario_armazena_senha_como_hash(app):
    usuario = criar_usuario(
        nome="Marinize",
        username="marinize",
        senha="senha-secreta",
    )

    assert usuario.senha_hash != "senha-secreta"
    assert check_password_hash(
        usuario.senha_hash,
        "senha-secreta",
    )


def test_criar_usuario_exige_nome(app):
    with pytest.raises(
        ValueError,
        match="O nome é obrigatório.",
    ):
        criar_usuario(
            nome="",
            username="marinize",
            senha="123456",
        )


def test_criar_usuario_exige_username(app):
    with pytest.raises(
        ValueError,
        match="O username é obrigatório.",
    ):
        criar_usuario(
            nome="Marinize",
            username="",
            senha="123456",
        )


def test_criar_usuario_exige_senha(app):
    with pytest.raises(
        ValueError,
        match="A senha é obrigatória.",
    ):
        criar_usuario(
            nome="Marinize",
            username="marinize",
            senha="",
        )


def test_criar_usuario_rejeita_perfil_invalido(app):
    with pytest.raises(
        ValueError,
        match="Perfil de usuário inválido.",
    ):
        criar_usuario(
            nome="Marinize",
            username="marinize",
            senha="123456",
            perfil="GERENTE",
        )


def test_criar_usuario_rejeita_username_duplicado(app):
    criar_usuario(
        nome="Marinize",
        username="marinize",
        senha="123456",
    )

    with pytest.raises(
        ValueError,
        match="Esse username já está cadastrado.",
    ):
        criar_usuario(
            nome="Outra Pessoa",
            username="marinize",
            senha="654321",
        )


def test_usuario_comum_pode_ser_inativado(app):
    admin = criar_usuario(
        nome="Admin",
        username="admin",
        senha="123456",
        perfil="ADMIN",
    )

    comum = criar_usuario(
        nome="Comum",
        username="comum",
        senha="123456",
        perfil="COMUM",
    )

    assert pode_inativar_usuario(comum, admin) is True

    inativar_usuario(comum, admin)

    assert comum.ativo is False


def test_usuario_nao_pode_inativar_a_propria_conta(app):
    usuario = criar_usuario(
        nome="Admin",
        username="admin",
        senha="123456",
        perfil="ADMIN",
    )

    with pytest.raises(
        ValueError,
        match="Você não pode inativar a própria conta.",
    ):
        inativar_usuario(usuario, usuario)


def test_ultimo_admin_nao_pode_ser_inativado(app):
    admin = criar_usuario(
        nome="Admin",
        username="admin",
        senha="123456",
        perfil="ADMIN",
    )

    outro_usuario = criar_usuario(
        nome="Comum",
        username="comum",
        senha="123456",
        perfil="COMUM",
    )

    assert pode_inativar_usuario(admin, outro_usuario) is False

    with pytest.raises(
        ValueError,
        match="O sistema precisa ter pelo menos um Admin ativo.",
    ):
        inativar_usuario(admin, outro_usuario)


def test_admin_pode_ser_inativado_se_existir_outro_admin(app):
    primeiro_admin = criar_usuario(
        nome="Primeiro Admin",
        username="admin1",
        senha="123456",
        perfil="ADMIN",
    )

    segundo_admin = criar_usuario(
        nome="Segundo Admin",
        username="admin2",
        senha="123456",
        perfil="ADMIN",
    )

    assert pode_inativar_usuario(
        primeiro_admin,
        segundo_admin,
    ) is True

    inativar_usuario(
        primeiro_admin,
        segundo_admin,
    )

    assert primeiro_admin.ativo is False
    assert segundo_admin.ativo is True


def test_ativar_usuario(app):
    admin = criar_usuario(
        nome="Admin",
        username="admin",
        senha="123456",
        perfil="ADMIN",
    )

    comum = criar_usuario(
        nome="Comum",
        username="comum",
        senha="123456",
        perfil="COMUM",
    )

    inativar_usuario(comum, admin)

    assert comum.ativo is False

    ativar_usuario(comum)

    assert comum.ativo is True


def test_editar_usuario(app):
    usuario = criar_usuario(
        nome="Nome Antigo",
        username="antigo",
        senha="123456",
    )

    editar_usuario(
        usuario,
        nome="Nome Novo",
        username="novo",
        perfil="ADMIN",
    )

    assert usuario.nome == "Nome Novo"
    assert usuario.username == "novo"
    assert usuario.perfil == "ADMIN"


def test_admin_nao_pode_ser_rebaixado_se_for_o_unico_admin(app):
    admin = criar_usuario(
        nome="Admin",
        username="admin",
        senha="123456",
        perfil="ADMIN",
    )

    with pytest.raises(
        ValueError,
        match="O sistema precisa ter pelo menos um Admin ativo.",
    ):
        editar_usuario(
            admin,
            nome="Admin",
            username="admin",
            perfil="COMUM",
        )


def test_admin_pode_ser_rebaixado_se_existir_outro_admin(app):
    primeiro_admin = criar_usuario(
        nome="Primeiro Admin",
        username="admin1",
        senha="123456",
        perfil="ADMIN",
    )

    criar_usuario(
        nome="Segundo Admin",
        username="admin2",
        senha="123456",
        perfil="ADMIN",
    )

    editar_usuario(
        primeiro_admin,
        nome="Primeiro Admin",
        username="admin1",
        perfil="COMUM",
    )

    assert primeiro_admin.perfil == "COMUM"


def test_editar_usuario_rejeita_username_duplicado(app):
    primeiro = criar_usuario(
        nome="Primeiro",
        username="primeiro",
        senha="123456",
    )

    criar_usuario(
        nome="Segundo",
        username="segundo",
        senha="123456",
    )

    with pytest.raises(
        ValueError,
        match="Esse username já está cadastrado.",
    ):
        editar_usuario(
            primeiro,
            nome="Primeiro",
            username="segundo",
            perfil="COMUM",
        )