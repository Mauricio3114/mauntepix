from datetime import datetime
from decimal import Decimal

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.parcela import Parcela
from app.models.pagamento import Pagamento

import os
from werkzeug.utils import secure_filename
from flask import current_app

from app.models.configpix import ConfigPix


parcelas_bp = Blueprint("parcelas", __name__)


@parcelas_bp.route("/parcelas")
@login_required
def listar_parcelas():
    parcelas = Parcela.query.filter_by(
        empresa_id=current_user.empresa_id
    ).order_by(
        Parcela.vencimento.asc()
    ).all()

    return render_template(
        "parcelas.html",
        parcelas=parcelas
    )


@parcelas_bp.route("/parcelas/<int:id>/receber", methods=["GET", "POST"])
@login_required
def receber_parcela(id):
    parcela = Parcela.query.filter_by(
        id=id,
        empresa_id=current_user.empresa_id
    ).first_or_404()

    if request.method == "POST":
        valor_pago = Decimal(
            request.form.get("valor_pago", "0")
            .replace(".", "")
            .replace(",", ".")
        )

        pagamento = Pagamento(
            empresa_id=current_user.empresa_id,
            parcela_id=parcela.id,
            cliente_id=parcela.cliente_id,
            valor_pago=valor_pago,
            forma_pagamento=request.form.get("forma_pagamento"),
            data_pagamento=datetime.utcnow(),
            status="confirmado"
        )

        parcela.status = "paga"
        parcela.data_pagamento = datetime.utcnow()
        parcela.valor_atualizado = valor_pago

        db.session.add(pagamento)
        db.session.commit()

        flash("Parcela recebida com sucesso!", "sucesso")
        return redirect(url_for("emprestimos.detalhes_parcelamento", id=parcela.emprestimo_id))

    return render_template("receber_parcela.html", parcela=parcela)



@parcelas_bp.route("/pagamentos/pendentes")
@login_required
def pagamentos_pendentes():
    pagamentos = Pagamento.query.filter_by(
        empresa_id=current_user.empresa_id,
        status="aguardando_confirmacao"
    ).order_by(Pagamento.id.desc()).all()

    return render_template("pagamentos_pendentes.html", pagamentos=pagamentos)


@parcelas_bp.route("/pagamentos/<int:id>/confirmar")
@login_required
def confirmar_pagamento(id):
    pagamento = Pagamento.query.filter_by(
        id=id,
        empresa_id=current_user.empresa_id
    ).first_or_404()

    pagamento.status = "confirmado"
    pagamento.parcela.status = "paga"
    pagamento.parcela.data_pagamento = datetime.utcnow()

    db.session.commit()

    flash("Pagamento confirmado com sucesso!", "sucesso")
    return redirect(url_for("parcelas.pagamentos_pendentes"))


@parcelas_bp.route("/pagar/<token>", methods=["GET", "POST"])
def pagar_parcela(token):
    parcela = Parcela.query.filter_by(
        token_pagamento=token
    ).first_or_404()

    if request.method == "POST":
        arquivo = request.files.get("comprovante")

        if not arquivo:
            flash("Envie o comprovante.", "erro")
            return redirect(request.url)

        pasta = os.path.join("app", "static", "uploads", "comprovantes")
        os.makedirs(pasta, exist_ok=True)

        nome = secure_filename(arquivo.filename)
        caminho = os.path.join(pasta, nome)
        arquivo.save(caminho)

        pagamento = Pagamento(
            empresa_id=parcela.empresa_id,
            parcela_id=parcela.id,
            cliente_id=parcela.cliente_id,
            valor_pago=parcela.valor_atualizado,
            forma_pagamento="pix",
            comprovante=f"uploads/comprovantes/{nome}",
            status="aguardando_confirmacao"
        )

        parcela.status = "aguardando_confirmacao"

        db.session.add(pagamento)
        db.session.commit()

        return render_template(
            "comprovante_enviado.html",
            parcela=parcela
        )

    config_pix = ConfigPix.query.filter_by(
        empresa_id=parcela.empresa_id,
        ativo=True
    ).first()

    return render_template(
        "devedor_pagar.html",
        parcela=parcela,
        config_pix=config_pix
    )