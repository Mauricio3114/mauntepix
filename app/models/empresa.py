from datetime import datetime
from app import db


class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(150))
    plano = db.Column(db.String(50), default="start")
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)