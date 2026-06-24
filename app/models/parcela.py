from app import db
import uuid


class Parcela(db.Model):
    __tablename__ = "parcelas"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    emprestimo_id = db.Column(db.Integer, db.ForeignKey("emprestimos.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    numero = db.Column(db.Integer, nullable=False)
    valor = db.Column(db.Numeric(12, 2), nullable=False)

    vencimento = db.Column(db.Date, nullable=False)
    data_pagamento = db.Column(db.DateTime)

    valor_multa = db.Column(db.Numeric(12, 2), default=0)
    dias_atraso = db.Column(db.Integer, default=0)
    valor_atualizado = db.Column(db.Numeric(12, 2), nullable=False)

    status = db.Column(db.String(20), default="aberta")

    empresa = db.relationship("Empresa", backref="parcelas")
    emprestimo = db.relationship("Emprestimo", backref="parcelas")
    cliente = db.relationship("Cliente", backref="parcelas")

    token_pagamento = db.Column(
        db.String(80),
        default=lambda: str(uuid.uuid4()),
        index=True
    )