from datetime import datetime
from app import db


class Emprestimo(db.Model):
    __tablename__ = "emprestimos"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    valor_liberado = db.Column(db.Numeric(12, 2), nullable=False)
    percentual_juros = db.Column(db.Numeric(5, 2), nullable=False)
    valor_total = db.Column(db.Numeric(12, 2), nullable=False)

    quantidade_parcelas = db.Column(db.Integer, nullable=False)
    periodicidade = db.Column(db.String(30), nullable=False)

    multa_dia = db.Column(db.Numeric(10, 2), default=0)
    data_inicio = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(30), default="ativo")
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship("Empresa", backref="emprestimos")
    cliente = db.relationship("Cliente", backref="emprestimos")