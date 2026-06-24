from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.empresa import Empresa
from app.models.configpix import ConfigPix


configuracoes_bp = Blueprint("configuracoes", __name__)


@configuracoes_bp.route("/configuracoes", methods=["GET", "POST"])
@login_required
def configuracoes():
    empresa = Empresa.query.get_or_404(current_user.empresa_id)

    config_pix = ConfigPix.query.filter_by(
        empresa_id=current_user.empresa_id
    ).first()

    if not config_pix:
        config_pix = ConfigPix(
            empresa_id=current_user.empresa_id,
            ativo=True
        )
        db.session.add(config_pix)
        db.session.commit()

    if request.method == "POST":
        empresa.nome = request.form.get("nome")
        empresa.cnpj = request.form.get("cnpj")
        empresa.telefone = request.form.get("telefone")
        empresa.email = request.form.get("email")

        config_pix.chave_pix = request.form.get("chave_pix")
        config_pix.public_key = request.form.get("public_key")
        config_pix.access_token = request.form.get("access_token")
        config_pix.ativo = True if request.form.get("pix_ativo") == "on" else False

        db.session.commit()

        flash("Configurações atualizadas com sucesso.", "sucesso")
        return redirect(url_for("configuracoes.configuracoes"))

    return render_template(
        "configuracoes.html",
        empresa=empresa,
        config_pix=config_pix
    )