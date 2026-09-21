import logging
from functools import wraps

from flask import (
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.models.usuario import Usuario


logger = logging.getLogger(__name__)


def _usuario_atual():
    """Obtém o usuário atual a partir da sessão."""

    usuario_id = session.get("usuario_id")

    if usuario_id is None:
        return None

    usuario = Usuario.query.get(usuario_id)

    if usuario is None:
        logger.warning(
            "Sessão associada a usuário inexistente: "
            "usuario_id=%s rota=%s",
            usuario_id,
            request.path,
        )

        session.clear()

        return None

    if not usuario.ativo:
        logger.warning(
            "Sessão de usuário inativo encerrada: "
            "usuario_id=%s username=%s rota=%s",
            usuario.id,
            usuario.username,
            request.path,
        )

        session.clear()

        return None

    session["usuario_nome"] = usuario.nome
    session["usuario_perfil"] = usuario.perfil

    return usuario


def login_required(view):
    """Exige que o usuário esteja autenticado e ativo."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        usuario = _usuario_atual()

        if usuario is None:
            logger.info(
                "Acesso não autenticado redirecionado para login: "
                "rota=%s",
                request.path,
            )

            return redirect(
                url_for("auth.login")
            )

        return view(*args, **kwargs)

    return wrapped_view

def escrita_required(view):
    """Exige autenticação e bloqueia o perfil DEMO em operações de escrita."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        usuario = _usuario_atual()

        if usuario is None:
            return redirect(url_for("auth.login"))

        if usuario.perfil == "DEMO":
            return render_template("403.html"), 403

        return view(*args, **kwargs)

    return wrapped_view


def admin_required(view):
    """Exige que o usuário autenticado seja administrador."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        usuario = _usuario_atual()

        if usuario is None:
            logger.info(
                "Acesso administrativo sem autenticação: "
                "rota=%s",
                request.path,
            )

            return redirect(
                url_for("auth.login")
            )

        if usuario.perfil != "ADMIN":
            logger.warning(
                "Acesso administrativo negado: "
                "usuario_id=%s username=%s perfil=%s rota=%s",
                usuario.id,
                usuario.username,
                usuario.perfil,
                request.path,
            )

            return render_template(
                "403.html"
            ), 403

        return view(*args, **kwargs)
    return wrapped_view