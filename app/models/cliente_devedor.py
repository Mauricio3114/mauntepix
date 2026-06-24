from datetime import datetime
from app import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    nome = db.Column(db.String(200), nullable=False)

    cpf = db.Column(db.String(20), nullable=False)

    rg = db.Column(db.String(30))

    data_nascimento = db.Column(db.Date)

    telefone = db.Column(db.String(30), nullable=False)

    whatsapp = db.Column(db.String(30))

    email = db.Column(db.String(150))

    cep = db.Column(db.String(20))

    logradouro = db.Column(db.String(200))

    numero = db.Column(db.String(30))

    complemento = db.Column(db.String(150))

    bairro = db.Column(db.String(120))

    cidade = db.Column(db.String(120))

    estado = db.Column(db.String(2))

    endereco = db.Column(db.String(250))

    senha = db.Column(db.String(255))

    ativo = db.Column(db.Boolean, default=True)

    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship("Empresa", backref="clientes")