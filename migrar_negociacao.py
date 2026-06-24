from app import create_app, db
from app.models.solicitacao_negociacao import SolicitacaoNegociacao

app = create_app()

with app.app_context():
    db.create_all()
    print("Tabela de negociações criada.")