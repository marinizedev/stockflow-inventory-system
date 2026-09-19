from flask import (
    Blueprint, 
    render_template, 
    request, 
    redirect, 
    url_for,
    session
)

from app.auth.decorators import admin_required
from app.models.usuario import Usuario

from app.services.usuario_service import ( 
    criar_usuario,
    inativar_usuario,
    ativar_usuario,
    editar_usuario
)


usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios")
@admin_required
def index():
    """Exibe a área de gerenciamento de usuários."""

    usuarios = Usuario.query.order_by(
        Usuario.nome
    ).all()

    return render_template(
        "usuarios/index.html",
        usuarios=usuarios,
    )


@usuarios_bp.route("/usuarios/novo", methods=["GET", "POST"])
@admin_required
def novo():
    """Exibe e processa o cadastro de um novo usuário."""

    if request.method == "POST":
        nome = request.form.get("nome", "")
        username = request.form.get("username", "")
        senha = request.form.get("senha", "")
        perfil = request.form.get("perfil", "COMUM")

        try:
            criar_usuario(
                nome=nome,
                username=username,
                senha=senha,
                perfil=perfil,
            )

            return redirect(url_for("usuarios.index"))

        except ValueError as erro:
            return render_template(
                "usuarios/novo.html",
                erro=str(erro),
                nome=nome,
                username=username,
                perfil=perfil,
            )

    return render_template("usuarios/novo.html")

@usuarios_bp.route("/usuarios/<int:usuario_id>/inativar", methods=["POST"])
@admin_required
def inativar(usuario_id):
    """Inativa um usuário por meio do gerenciamento administrativo."""

    usuario = Usuario.query.get_or_404(usuario_id)

    usuario_logado = Usuario.query.get_or_404(
        session["usuario_id"]
    )

    try:
        inativar_usuario(
            usuario=usuario,
            usuario_logado=usuario_logado,
        )

    except ValueError as erro:
        return render_template(
            "usuarios/index.html",
            usuarios=Usuario.query.order_by(
                Usuario.nome
            ).all(),
            erro=str(erro),
        )

    return redirect(url_for("usuarios.index"))

@usuarios_bp.route("/usuarios/<int:usuario_id>/ativar", methods=["POST"])
@admin_required
def ativar(usuario_id):
    """Ativa um usuário por meio do gerenciamento administrativo."""

    usuario = Usuario.query.get_or_404(usuario_id)

    ativar_usuario(usuario)

    return redirect(url_for("usuarios.index"))

@usuarios_bp.route(
    "/usuarios/<int:usuario_id>/editar",
    methods=["GET", "POST"],
)
@admin_required
def editar(usuario_id):
    """Exibe e processa a edição de um usuário."""

    usuario = Usuario.query.get_or_404(usuario_id)

    if request.method == "POST":
        nome = request.form.get("nome", "")
        username = request.form.get("username", "")
        perfil = request.form.get("perfil", "COMUM")

        try:
            editar_usuario(
                usuario=usuario,
                nome=nome,
                username=username,
                perfil=perfil,
            )

            return redirect(url_for("usuarios.index"))

        except ValueError as erro:
            return render_template(
                "usuarios/editar.html",
                usuario=usuario,
                erro=str(erro),
                nome=nome,
                username=username,
                perfil=perfil,
            )

    return render_template(
        "usuarios/editar.html",
        usuario=usuario,
        nome=usuario.nome,
        username=usuario.username,
        perfil=usuario.perfil,
    )