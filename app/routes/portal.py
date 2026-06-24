from datetime import date

from flask import Blueprint, render_template, redirect, url_for
from sqlalchemy.orm import joinedload

from app.models.cliente_devedor import Cliente
from app.models.parcela import Parcela
from app.models.empresa import Empresa
from app.models.configpix import ConfigPix


portal_bp = Blueprint("portal", __name__)


@portal_bp.route("/portal/<token>")
def portal_cliente(token):
    cliente = Cliente.query.filter_by(
        token_portal=token,
        ativo=True
    ).first_or_404()

    empresa = Empresa.query.get(cliente.empresa_id)

    config_pix = ConfigPix.query.filter_by(
        empresa_id=cliente.empresa_id
    ).first()

    hoje = date.today()

    parcelas = Parcela.query.options(
        joinedload(Parcela.emprestimo)
    ).filter_by(
        empresa_id=cliente.empresa_id,
        cliente_id=cliente.id
    ).order_by(
        Parcela.vencimento.asc()
    ).all()

    abertas = [
        p for p in parcelas
        if p.status != "paga"
    ]

    pagas = [
        p for p in parcelas
        if p.status == "paga"
    ]

    atrasadas = [
        p for p in abertas
        if p.vencimento and p.vencimento < hoje
    ]

    parcela_para_pagar = None

    if atrasadas:
        parcela_para_pagar = atrasadas[0]
    elif abertas:
        parcela_para_pagar = abertas[0]

    saldo_devedor = sum([
        float(p.valor_atualizado or p.valor or 0)
        for p in abertas
    ])

    total_pago = sum([
        float(p.valor_atualizado or p.valor or 0)
        for p in pagas
    ])

    return render_template(
        "portal_cliente.html",
        cliente=cliente,
        empresa=empresa,
        config_pix=config_pix,
        parcelas=parcelas,
        abertas=abertas,
        pagas=pagas,
        atrasadas=atrasadas,
        parcela_para_pagar=parcela_para_pagar,
        saldo_devedor=saldo_devedor,
        total_pago=total_pago,
        hoje=hoje
    )