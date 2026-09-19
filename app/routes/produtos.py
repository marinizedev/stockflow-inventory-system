from decimal import Decimal, InvalidOperation

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)

from app.auth.decorators import admin_required, login_required
from app.models.produto import Produto
from app.services.produto_service import (
    ativar_produto,
    criar_produto,
    editar_produto,
    inativar_produto,
)


produtos_bp = Blueprint("produtos", __name__)


@produtos_bp.route("/produtos")
@login_required
def index():
    """Exibe os produtos cadastrados."""

    produtos = Produto.query.order_by(
        Produto.nome
    ).all()

    return render_template(
        "produtos/index.html",
        produtos=produtos,
    )


@produtos_bp.route("/produtos/novo", methods=["GET", "POST"])
@admin_required
def novo():
    """Exibe e processa o cadastro de um novo produto."""

    if request.method == "POST":

        codigo = request.form.get("codigo", "")
        nome = request.form.get("nome", "")
        descricao = request.form.get("descricao", "")
        categoria = request.form.get("categoria", "")
        quantidade_inicial = request.form.get(
            "quantidade_inicial",
            "",
        )
        estoque_minimo = request.form.get(
            "estoque_minimo",
            "",
        )
        preco = request.form.get("preco", "")

        try:
            quantidade_inicial = int(quantidade_inicial)
            estoque_minimo = int(estoque_minimo)
            preco = Decimal(preco)

            criar_produto(
                codigo=codigo,
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                quantidade_inicial=quantidade_inicial,
                estoque_minimo=estoque_minimo,
                preco=preco,
            )

            return redirect(url_for("produtos.index"))

        except ValueError as erro:
            return render_template(
                "produtos/novo.html",
                erro=str(erro),
                codigo=codigo,
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                quantidade_inicial=quantidade_inicial,
                estoque_minimo=estoque_minimo,
                preco=preco,
            )

        except InvalidOperation:
            return render_template(
                "produtos/novo.html",
                erro="Informe um preço válido.",
                codigo=codigo,
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                quantidade_inicial=quantidade_inicial,
                estoque_minimo=estoque_minimo,
                preco=preco,
            )

    return render_template("produtos/novo.html")


@produtos_bp.route(
    "/produtos/<int:produto_id>/editar",
    methods=["GET", "POST"],
)
@admin_required
def editar(produto_id):
    """Exibe e processa a edição de um produto."""

    produto = Produto.query.get_or_404(produto_id)

    if request.method == "POST":

        codigo = request.form.get("codigo", "")
        nome = request.form.get("nome", "")
        descricao = request.form.get("descricao", "")
        categoria = request.form.get("categoria", "")
        estoque_minimo = request.form.get(
            "estoque_minimo",
            "",
        )
        preco = request.form.get("preco", "")

        try:
            estoque_minimo = int(estoque_minimo)
            preco = Decimal(preco)

            editar_produto(
                produto=produto,
                codigo=codigo,
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                estoque_minimo=estoque_minimo,
                preco=preco,
            )

            return redirect(url_for("produtos.index"))

        except ValueError as erro:
            return render_template(
                "produtos/editar.html",
                erro=str(erro),
                produto=produto,
                codigo=codigo,
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                estoque_minimo=estoque_minimo,
                preco=preco,
            )

        except InvalidOperation:
            return render_template(
                "produtos/editar.html",
                erro="Informe um preço válido.",
                produto=produto,
                codigo=codigo,
                nome=nome,
                descricao=descricao,
                categoria=categoria,
                estoque_minimo=estoque_minimo,
                preco=preco,
            )

    return render_template(
        "produtos/editar.html",
        produto=produto,
        codigo=produto.codigo,
        nome=produto.nome,
        descricao=produto.descricao or "",
        categoria=produto.categoria or "",
        estoque_minimo=produto.estoque_minimo,
        preco=produto.preco,
    )


@produtos_bp.route(
    "/produtos/<int:produto_id>/inativar",
    methods=["POST"],
)
@admin_required
def inativar(produto_id):
    """Inativa um produto."""

    produto = Produto.query.get_or_404(produto_id)

    inativar_produto(produto)

    return redirect(url_for("produtos.index"))


@produtos_bp.route(
    "/produtos/<int:produto_id>/ativar",
    methods=["POST"],
)
@admin_required
def ativar(produto_id):
    """Ativa um produto."""

    produto = Produto.query.get_or_404(produto_id)

    ativar_produto(produto)

    return redirect(url_for("produtos.index"))