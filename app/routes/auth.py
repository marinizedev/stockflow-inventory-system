from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

from app.models.usuario import Usuario


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Realiza a autenticação do usuário."""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        senha = request.form.get("senha", "")

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

            return redirect(url_for("dashboard.index"))

        return render_template(
            "login.html",
            erro="Username ou senha inválidos.",
        )

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    """Encerra a sessão do usuário autenticado."""

    session.clear()

    return redirect(url_for("auth.login"))