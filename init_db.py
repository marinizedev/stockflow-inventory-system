from app import create_app, db
from app.models.movimentacao import Movimentacao
from app.models.produto import Produto
from app.models.usuario import Usuario


app = create_app()

with app.app_context():
    db.create_all()

print("Banco de dados criado com sucesso!")