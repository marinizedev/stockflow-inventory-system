from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

from config import Config


db = SQLAlchemy()


def configurar_sqlite(engine):
    """Configura o SQLite para aplicar as Foreign Keys."""

    if engine.dialect.name != "sqlite":
        return

    @event.listens_for(engine, "connect")
    def ativar_foreign_keys(
        dbapi_connection,
        connection_record,
    ):
        """Ativa a integridade referencial do SQLite."""

        cursor = dbapi_connection.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        cursor.close()


def create_app():
    """Cria e configura a aplicação Flask."""

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        configurar_sqlite(db.engine)

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.produtos import produtos_bp
    from app.routes.movimentacoes import movimentacoes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(movimentacoes_bp)

    return app