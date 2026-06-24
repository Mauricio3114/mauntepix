from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Usuario(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=True
    )

    nome = db.Column(db.String(150), nullable=False)

    email = db.Column(db.String(150), unique=True, nullable=False)

    senha_hash = db.Column(db.String(255), nullable=False)

    perfil = db.Column(db.String(30), default="admin")

    ativo = db.Column(db.Boolean, default=True)

    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship("Empresa", backref="usuarios")

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def is_master(self):
        return self.perfil == "master"

    def is_admin(self):
        return self.perfil in ["master", "admin"]


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))