from datetime import datetime
from app import db


class Pagamento(db.Model):
    __tablename__ = "pagamentos"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    parcela_id = db.Column(db.Integer, db.ForeignKey("parcelas.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    valor_pago = db.Column(db.Numeric(12, 2), nullable=False)
    data_pagamento = db.Column(db.DateTime, default=datetime.utcnow)

    forma_pagamento = db.Column(db.String(50), default="pix")
    comprovante = db.Column(db.String(500))
    status = db.Column(db.String(30), default="confirmado")

    parcela = db.relationship("Parcela", backref="pagamentos")