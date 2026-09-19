from functools import wraps

from flask import ( 
    redirect,
    render_template, 
    session, 
    url_for,
)

from app.models.usuario import Usuario


def _usuario_atual():
    """Obtém o usuário atual a partir da sessão."""

    usuario_id = session.get("usuario_id")

    if usuario_id is None:
        return None

    usuario = Usuario.query.get(usuario_id)

    if usuario is None or not usuario.ativo:
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
            return redirect(url_for("auth.login"))

        return view(*args, **kwargs)

    return wrapped_view


def admin_required(view):
    """Exige que o usuário autenticado seja administrador."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        usuario = _usuario_atual()

        if usuario is None:
            return redirect(url_for("auth.login"))

        if usuario.perfil != "ADMIN":
            return render_template("403.html"), 403

        return view(*args, **kwargs)

    return wrapped_view