from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.configpix import ConfigPix

pix_bp = Blueprint("pix", __name__)


@pix_bp.route("/configuracoes/pix", methods=["GET", "POST"])
@login_required
def configuracao_pix():

    config = ConfigPix.query.filter_by(
        empresa_id=current_user.empresa_id
    ).first()

    if not config:
        config = ConfigPix(
            empresa_id=current_user.empresa_id
        )
        db.session.add(config)
        db.session.commit()

    if request.method == "POST":

        config.chave_pix = request.form.get("chave_pix")

        db.session.commit()

        flash(
            "Chave PIX salva com sucesso.",
            "sucesso"
        )

        return redirect(
            url_for("pix.configuracao_pix")
        )

    return render_template(
        "config_pix.html",
        config=config
    )