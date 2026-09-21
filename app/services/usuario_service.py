import logging

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from app import db
from app.models.usuario import Usuario


logger = logging.getLogger(__name__)


def criar_usuario(
    nome,
    username,
    senha,
    perfil="COMUM",
):
    """Cria um novo usuário respeitando as regras de negócio."""

    nome = nome.strip()
    username = username.strip()

    if not nome:
        raise ValueError("O nome é obrigatório.")

    if not username:
        raise ValueError("O username é obrigatório.")

    if not senha:
        raise ValueError("A senha é obrigatória.")

    if perfil not in {"ADMIN", "COMUM", "DEMO"}:
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

        logger.exception(
            "Erro ao criar usuário: username=%s perfil=%s",
            username,
            perfil,
        )

        raise

    logger.info(
        "Usuário criado com sucesso: "
        "usuario_id=%s username=%s perfil=%s",
        usuario.id,
        usuario.username,
        usuario.perfil,
    )

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
        logger.warning(
            "Tentativa de auto-inativação bloqueada: "
            "usuario_id=%s",
            usuario.id,
        )

        raise ValueError(
            "Você não pode inativar a própria conta."
        )

    if not pode_inativar_usuario(
        usuario,
        usuario_logado,
    ):
        logger.warning(
            "Inativação bloqueada para preservar "
            "o último administrador: usuario_id=%s",
            usuario.id,
        )

        raise ValueError(
            "O sistema precisa ter pelo menos um Admin ativo."
        )

    usuario.ativo = False

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        logger.exception(
            "Erro ao inativar usuário: "
            "usuario_id=%s username=%s",
            usuario.id,
            usuario.username,
        )

        raise

    logger.info(
        "Usuário inativado com sucesso: "
        "usuario_id=%s username=%s",
        usuario.id,
        usuario.username,
    )


def ativar_usuario(usuario):
    """Ativa um usuário."""

    if usuario.ativo:
        logger.info(
            "Usuário já estava ativo: "
            "usuario_id=%s username=%s",
            usuario.id,
            usuario.username,
        )

        return

    usuario.ativo = True

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()

        logger.exception(
            "Erro ao ativar usuário: "
            "usuario_id=%s username=%s",
            usuario.id,
            usuario.username,
        )

        raise

    logger.info(
        "Usuário ativado com sucesso: "
        "usuario_id=%s username=%s",
        usuario.id,
        usuario.username,
    )


def editar_usuario(
    usuario,
    nome,
    username,
    perfil,
):
    """Edita um usuário respeitando as regras de negócio."""

    nome = nome.strip()
    username = username.strip()

    if not nome:
        raise ValueError("O nome é obrigatório.")

    if not username:
        raise ValueError("O username é obrigatório.")

    if perfil not in {"ADMIN", "COMUM", "DEMO"}:
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
        and perfil != "ADMIN"
        and usuario.ativo
    ):
        quantidade_outros_admins = Usuario.query.filter(
            Usuario.perfil == "ADMIN",
            Usuario.ativo.is_(True),
            Usuario.id != usuario.id,
        ).count()

        if quantidade_outros_admins == 0:
            logger.warning(
                "Edição bloqueada para preservar "
                "o último administrador: usuario_id=%s",
                usuario.id,
            )

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

        logger.exception(
            "Erro ao editar usuário: "
            "usuario_id=%s username=%s",
            usuario.id,
            usuario.username,
        )

        raise

    logger.info(
        "Usuário editado com sucesso: "
        "usuario_id=%s username=%s perfil=%s",
        usuario.id,
        usuario.username,
        usuario.perfil,
    )
