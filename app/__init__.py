from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para continuar."

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "mauntepix123"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mauntepix.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # IMPORTA TODOS OS MODELS SEPARADOS
    from app.models.empresa import Empresa
    from app.models.usuario import Usuario
    from app.models.cliente_devedor import Cliente
    from app.models.emprestimo import Emprestimo
    from app.models.parcela import Parcela
    from app.models.pagamento import Pagamento
    from app.models.configpix import ConfigPix

    # ROTAS
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.clientes import clientes_bp
    from app.routes.emprestimos import emprestimos_bp
    from app.routes.parcelas import parcelas_bp
    from app.routes.pix import pix_bp
    from app.routes.relatorios import relatorios_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.configuracoes import configuracoes_bp
    from app.routes.master import master_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(emprestimos_bp)
    app.register_blueprint(parcelas_bp)
    app.register_blueprint(pix_bp)
    app.register_blueprint(relatorios_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(configuracoes_bp)
    app.register_blueprint(master_bp)

    return app