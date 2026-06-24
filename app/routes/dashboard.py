from datetime import date
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

from app.models.cliente_devedor import Cliente
from app.models.emprestimo import Emprestimo
from app.models.parcela import Parcela
from app.models.pagamento import Pagamento

dashboard_bp = Blueprint("dashboard", __name__)


def db_valor(valor):
    return float(valor or 0)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    empresa_id = current_user.empresa_id
    hoje = date.today()

    total_clientes = Cliente.query.filter_by(empresa_id=empresa_id).count()
    total_emprestimos = Emprestimo.query.filter_by(empresa_id=empresa_id).count()

    total_emprestado = db_valor(
        Emprestimo.query.with_entities(func.sum(Emprestimo.valor_liberado))
        .filter_by(empresa_id=empresa_id)
        .scalar()
    )

    total_com_juros = db_valor(
        Emprestimo.query.with_entities(func.sum(Emprestimo.valor_total))
        .filter_by(empresa_id=empresa_id)
        .scalar()
    )

    total_recebido = db_valor(
        Pagamento.query.with_entities(func.sum(Pagamento.valor_pago))
        .filter(
            Pagamento.empresa_id == empresa_id,
            Pagamento.status == "confirmado"
        )
        .scalar()
    )

    total_aberto = total_com_juros - total_recebido
    lucro_previsto = total_com_juros - total_emprestado

    parcelas_abertas = Parcela.query.filter_by(
        empresa_id=empresa_id,
        status="aberta"
    ).count()

    parcelas_pagas = Parcela.query.filter_by(
        empresa_id=empresa_id,
        status="paga"
    ).count()

    parcelas_atrasadas = Parcela.query.filter(
        Parcela.empresa_id == empresa_id,
        Parcela.status == "aberta",
        Parcela.vencimento < hoje
    ).count()

    pagamentos_pendentes = Pagamento.query.filter_by(
        empresa_id=empresa_id,
        status="aguardando_confirmacao"
    ).count()

    total_parcelas = parcelas_abertas + parcelas_pagas + parcelas_atrasadas + pagamentos_pendentes

    return render_template(
        "dashboard.html",
        total_clientes=total_clientes,
        total_emprestimos=total_emprestimos,
        total_emprestado=total_emprestado,
        total_com_juros=total_com_juros,
        total_recebido=total_recebido,
        total_aberto=total_aberto,
        lucro_previsto=lucro_previsto,
        parcelas_abertas=parcelas_abertas,
        parcelas_pagas=parcelas_pagas,
        parcelas_atrasadas=parcelas_atrasadas,
        pagamentos_pendentes=pagamentos_pendentes,
        total_parcelas=total_parcelas,
    )