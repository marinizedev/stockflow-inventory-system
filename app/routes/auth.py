import logging

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)

from werkzeug.security import check_password_hash

from app.models.usuario import Usuario


logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Realiza a autenticação do usuário."""

    if request.method == "POST":
        username = request.form.get(
            "username",
            "",
        ).strip()

        senha = request.form.get(
            "senha",
            "",
        )

        usuario = Usuario.query.filter_by(
            username=username
        ).first()

        if usuario and usuario.ativo and check_password_hash(
            usuario.senha_hash,
            senha,
        ):
            session["usuario_id"] = usuario.id
            session["usuario_nome"] = usuario.nome
            session["usuario_perfil"] = usuario.perfil

            logger.info(
                "Login realizado com sucesso: "
                "usuario_id=%s username=%s perfil=%s",
                usuario.id,
                usuario.username,
                usuario.perfil,
            )

            return redirect(
                url_for("dashboard.index")
            )

        logger.warning(
            "Tentativa de login inválida: username=%s",
            username,
        )

        return render_template(
            "login.html",
            erro="Username ou senha inválidos.",
        )

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Encerra a sessão do usuário autenticado."""

    usuario_id = session.get("usuario_id")
    usuario_nome = session.get("usuario_nome")

    if usuario_id is not None:
        logger.info(
            "Logout realizado: usuario_id=%s nome=%s",
            usuario_id,
            usuario_nome,
        )

    session.clear()

    return redirect(url_for("auth.login"))
