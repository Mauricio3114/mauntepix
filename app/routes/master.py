from datetime import date, timedelta

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models.empresa import Empresa
from app.models.usuario import Usuario
from app.models.cliente_devedor import Cliente
from app.models.emprestimo import Emprestimo
from app.models.parcela import Parcela


master_bp = Blueprint("master", __name__)


def master_required():
    return current_user.is_authenticated and current_user.perfil == "master"


@master_bp.route("/master")
@login_required
def dashboard_master():
    if not master_required():
        flash("Acesso permitido apenas ao Admin Master.", "erro")
        return redirect(url_for("dashboard.dashboard"))

    hoje = date.today()
    limite = hoje + timedelta(days=5)

    empresas = Empresa.query.order_by(Empresa.data_cadastro.desc()).all()

    total_empresas = Empresa.query.count()
    empresas_ativas = Empresa.query.filter_by(ativo=True).count()
    empresas_inativas = Empresa.query.filter_by(ativo=False).count()

    vencidas = Empresa.query.filter(
        Empresa.data_vencimento < hoje
    ).count()

    vencendo = Empresa.query.filter(
        Empresa.data_vencimento >= hoje,
        Empresa.data_vencimento <= limite
    ).count()

    total_usuarios = Usuario.query.count()
    total_clientes_devedores = Cliente.query.count()
    total_parcelamentos = Emprestimo.query.count()
    total_parcelas = Parcela.query.count()

    return render_template(
        "master_dashboard.html",
        empresas=empresas,
        total_empresas=total_empresas,
        empresas_ativas=empresas_ativas,
        empresas_inativas=empresas_inativas,
        vencidas=vencidas,
        vencendo=vencendo,
        total_usuarios=total_usuarios,
        total_clientes_devedores=total_clientes_devedores,
        total_parcelamentos=total_parcelamentos,
        total_parcelas=total_parcelas,
        hoje=hoje
    )