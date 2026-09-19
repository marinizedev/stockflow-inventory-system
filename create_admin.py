from getpass import getpass

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.usuario import Usuario


def obter_dados_admin():
    """Solicita e valida os dados do administrador."""

    nome = input("Nome do administrador: ").strip()
    username = input("Username do administrador: ").strip()

    if not nome:
        raise ValueError("O nome é obrigatório.")

    if not username:
        raise ValueError("O username é obrigatório.")

    senha = getpass("Senha: ")
    confirmacao = getpass("Confirme a senha: ")

    if not senha:
        raise ValueError("A senha é obrigatória.")

    if senha != confirmacao:
        raise ValueError("As senhas não conferem.")

    return nome, username, senha


def criar_admin():
    """Cria o usuário administrador inicial do sistema."""

    nome, username, senha = obter_dados_admin()

    usuario_existente = Usuario.query.filter_by(
        username=username
    ).first()

    if usuario_existente:
        raise ValueError(
            "Esse username já está cadastrado."
        )

    senha_hash = generate_password_hash(senha)

    admin = Usuario(
        nome=nome,
        username=username,
        senha_hash=senha_hash,
        perfil="ADMIN",
        ativo=True,
    )

    db.session.add(admin)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise


app = create_app()

with app.app_context():
    try:
        criar_admin()
        print("\nAdministrador criado com sucesso!")

    except ValueError as erro:
        print(f"\nErro de validação: {erro}")

    except SQLAlchemyError:
        print(
            "\nErro: não foi possível salvar "
            "o administrador no banco de dados."
        )

    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")