from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.auth.decorators import login_required
from app.models.movimentacao import Movimentacao
from app.models.produto import Produto
from app.models.usuario import Usuario
from app.services.movimentacao_service import (
    registrar_movimentacao,
)

movimentacoes_bp = Blueprint(
    "movimentacoes",
    __name__,
)


@movimentacoes_bp.route("/movimentacoes")
@login_required
def index():
    """Exibe o histórico de movimentações."""

    movimentacoes = (
        Movimentacao.query
        .order_by(
            Movimentacao.realizado_em.desc()
        )
        .all()
    )

    return render_template(
        "movimentacoes/index.html",
        movimentacoes=movimentacoes,
    )


@movimentacoes_bp.route(
    "/movimentacoes/nova",
    methods=["GET", "POST"],
)
@login_required
def nova():
    """Exibe e processa uma nova movimentação."""

    produtos = (
        Produto.query
        .filter_by(ativo=True)
        .order_by(Produto.nome)
        .all()
    )

    if request.method == "POST":
        produto_id = request.form.get("produto_id", "")
        tipo = request.form.get("tipo", "")
        quantidade = request.form.get("quantidade", "")
        observacao = request.form.get("observacao", "")

        try:
            produto = Produto.query.get_or_404(
                int(produto_id)
            )

            quantidade = int(quantidade)

            usuario = Usuario.query.get_or_404(
                session["usuario_id"]
            )

            registrar_movimentacao(
                produto=produto,
                usuario=usuario,
                tipo=tipo,
                quantidade=quantidade,
                observacao=observacao,
            )

            return redirect(
                url_for("movimentacoes.index")
            )

        except ValueError as erro:
            return render_template(
                "movimentacoes/nova.html",
                erro=str(erro),
                produtos=produtos,
                produto_id=produto_id,
                tipo=tipo,
                quantidade=quantidade,
                observacao=observacao,
            )

    return render_template(
        "movimentacoes/nova.html",
        produtos=produtos,
    )