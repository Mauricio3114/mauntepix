from datetime import datetime
from app import db


class SolicitacaoNegociacao(db.Model):
    __tablename__ = "solicitacoes_negociacao"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresas.id"), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("clientes.id"), nullable=False)

    tipo = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Numeric(12, 2))
    observacao = db.Column(db.Text)

    status = db.Column(db.String(30), default="pendente")
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    empresa = db.relationship("Empresa", backref="solicitacoes_negociacao")
    cliente = db.relationship("Cliente", backref="solicitacoes_negociacao")