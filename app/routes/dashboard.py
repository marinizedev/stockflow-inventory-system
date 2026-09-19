from flask import Blueprint, render_template

from app.auth.decorators import login_required
from app.models.movimentacao import Movimentacao
from app.models.produto import Produto
from app.models.usuario import Usuario


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    """Exibe o painel principal do StockFlow."""

    total_produtos = Produto.query.count()

    produtos_estoque_baixo = Produto.query.filter(
        Produto.ativo.is_(True),
        Produto.quantidade_atual < Produto.estoque_minimo,
    ).order_by(
        Produto.quantidade_atual
    ).all()

    total_movimentacoes = Movimentacao.query.count()

    total_usuarios = Usuario.query.count()

    movimentacoes_recentes = (
        Movimentacao.query
        .order_by(
            Movimentacao.realizado_em.desc()
        )
        .limit(5)
        .all()
    )

    return render_template(
        "dashboard.html",
        total_produtos=total_produtos,
        produtos_estoque_baixo=produtos_estoque_baixo,
        total_movimentacoes=total_movimentacoes,
        total_usuarios=total_usuarios,
        movimentacoes_recentes=movimentacoes_recentes,
    )