from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from app import db
from app.models.usuario import Usuario

def criar_usuario(nome, username, senha, perfil="COMUM"):
    """Cria um novo usuário respeitando as regras de negócio."""

    nome = nome.strip()
    username = username.strip()

    if not nome:
        raise ValueError("O nome é obrigatório.")

    if not username:
        raise ValueError("O username é obrigatório.")

    if not senha:
        raise ValueError("A senha é obrigatória.")

    if perfil not in {"ADMIN", "COMUM"}:
        raise ValueError("Perfil de usuário inválido.")

    usuario_existente = Usuario.query.filter_by(
        username=username
    ).first()

    if usuario_existente:
        raise ValueError(
            "Esse username já está cadastrado."
        )

    usuario = Usuario(
        nome=nome,
        username=username,
        senha_hash=generate_password_hash(senha),
        perfil=perfil,
        ativo=True,
    )

    db.session.add(usuario)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise

    return usuario

def pode_inativar_usuario(usuario, usuario_logado):
    """Verifica se um usuário pode ser inativado."""

    if usuario.id == usuario_logado.id:
        return False

    if usuario.perfil != "ADMIN":
        return True

    if not usuario.ativo:
        return True

    quantidade_admins_ativos = Usuario.query.filter_by(
        perfil="ADMIN",
        ativo=True,
    ).count()

    return quantidade_admins_ativos > 1


def inativar_usuario(usuario, usuario_logado):
    """Inativa um usuário respeitando as regras de negócio."""

    if usuario.id == usuario_logado.id:
        raise ValueError(
            "Você não pode inativar a própria conta."
        )

    if not pode_inativar_usuario(usuario, usuario_logado):
        raise ValueError(
            "O sistema precisa ter pelo menos um Admin ativo."
        )

    usuario.ativo = False

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise

def ativar_usuario(usuario):
    """Ativa um usuário."""

    if usuario.ativo:
        return

    usuario.ativo = True

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise

def editar_usuario(usuario, nome, username, perfil):
    """Edita os dados de um usuário respeitando as regras de negócio."""

    nome = nome.strip()
    username = username.strip()

    if not nome:
        raise ValueError("O nome é obrigatório.")

    if not username:
        raise ValueError("O username é obrigatório.")

    if perfil not in {"ADMIN", "COMUM"}:
        raise ValueError("Perfil de usuário inválido.")

    usuario_existente = Usuario.query.filter(
        Usuario.username == username,
        Usuario.id != usuario.id,
    ).first()

    if usuario_existente:
        raise ValueError(
            "Esse username já está cadastrado."
        )

    if (
        usuario.perfil == "ADMIN"
        and perfil == "COMUM"
        and usuario.ativo
    ):
        quantidade_outros_admins = Usuario.query.filter(
            Usuario.perfil == "ADMIN",
            Usuario.ativo.is_(True),
            Usuario.id != usuario.id,
        ).count()

        if quantidade_outros_admins == 0:
            raise ValueError(
                "O sistema precisa ter pelo menos um Admin ativo."
            )

    usuario.nome = nome
    usuario.username = username
    usuario.perfil = perfil

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise