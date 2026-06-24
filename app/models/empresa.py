from datetime import datetime, date
from app import db


class Empresa(db.Model):
    __tablename__ = "empresas"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(20))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(150))

    plano = db.Column(db.String(50), default="start")
    valor_mensalidade = db.Column(db.Numeric(10, 2), default=0)
    data_vencimento = db.Column(db.Date)
    status_pagamento = db.Column(db.String(30), default="em_dia")

    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    def mensalidade_vencida(self):
        if not self.data_vencimento:
            return False

        return self.data_vencimento < date.today()

    def mensalidade_proxima(self):
        if not self.data_vencimento:
            return False

        dias = (self.data_vencimento - date.today()).days
        return 0 <= dias <= 5