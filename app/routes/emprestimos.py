from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from datetime import datetime, timedelta
from decimal import Decimal

from app import db

from app.models.cliente_devedor import Cliente
from app.models.emprestimo import Emprestimo
from app.models.parcela import Parcela


emprestimos_bp = Blueprint(
    "emprestimos",
    __name__
)


def calcular_proximo_vencimento(
    data_inicio,
    numero,
    periodicidade
):

    if periodicidade == "diario":
        return data_inicio + timedelta(days=numero - 1)

    if periodicidade == "semanal":
        return data_inicio + timedelta(days=(numero - 1) * 7)

    if periodicidade == "quinzenal":
        return data_inicio + timedelta(days=(numero - 1) * 15)

    if periodicidade == "dez_dias":
        return data_inicio + timedelta(days=(numero - 1) * 10)

    if periodicidade == "mensal":
        return data_inicio + timedelta(days=(numero - 1) * 30)

    return data_inicio


@emprestimos_bp.route("/parcelamentos")
@login_required
def parcelamentos():

    lista = Emprestimo.query.filter_by(
        empresa_id=current_user.empresa_id
    ).order_by(
        Emprestimo.id.desc()
    ).all()

    return render_template(
        "parcelamentos.html",
        parcelamentos=lista
    )


@emprestimos_bp.route(
    "/parcelamentos/novo",
    methods=["GET", "POST"]
)
@login_required
def novo_parcelamento():

    clientes = Cliente.query.filter_by(
        empresa_id=current_user.empresa_id
    ).order_by(
        Cliente.nome.asc()
    ).all()

    if request.method == "POST":

        cliente_id = int(
            request.form["cliente_id"]
        )

        valor_liberado = Decimal(
            request.form["valor_liberado"]
            .replace(".", "")
            .replace(",", ".")
        )

        percentual_juros = Decimal(
            request.form["percentual_juros"]
            .replace(",", ".")
        )

        quantidade_parcelas = int(
            request.form["quantidade_parcelas"]
        )

        periodicidade = request.form[
            "periodicidade"
        ]

        multa_dia = Decimal(
            request.form["multa_dia"]
            .replace(".", "")
            .replace(",", ".")
        )

        data_inicio = datetime.strptime(
            request.form["data_inicio"],
            "%Y-%m-%d"
        ).date()

        valor_total = (
            valor_liberado +
            (
                valor_liberado *
                percentual_juros / 100
            )
        )

        valor_parcela = (
            valor_total /
            quantidade_parcelas
        )

        emprestimo = Emprestimo(
            empresa_id=current_user.empresa_id,
            cliente_id=cliente_id,
            valor_liberado=valor_liberado,
            percentual_juros=percentual_juros,
            valor_total=valor_total,
            quantidade_parcelas=quantidade_parcelas,
            periodicidade=periodicidade,
            multa_dia=multa_dia,
            data_inicio=data_inicio,
            status="ativo"
        )

        db.session.add(emprestimo)
        db.session.flush()

        for numero in range(
            1,
            quantidade_parcelas + 1
        ):

            vencimento = calcular_proximo_vencimento(
                data_inicio,
                numero,
                periodicidade
            )

            parcela = Parcela(
                empresa_id=current_user.empresa_id,
                emprestimo_id=emprestimo.id,
                cliente_id=cliente_id,
                numero=numero,
                valor=valor_parcela,
                vencimento=vencimento,
                valor_atualizado=valor_parcela,
                status="aberta"
            )

            db.session.add(parcela)

        db.session.commit()

        flash(
            "Parcelamento criado com sucesso!",
            "sucesso"
        )

        return redirect(
            url_for(
                "emprestimos.parcelamentos"
            )
        )

    return render_template(
        "parcelamento_form.html",
        clientes=clientes
    )


@emprestimos_bp.route(
    "/parcelamentos/<int:id>"
)
@login_required
def detalhes_parcelamento(id):

    emprestimo = Emprestimo.query.filter_by(
        id=id,
        empresa_id=current_user.empresa_id
    ).first_or_404()

    parcelas = Parcela.query.filter_by(
        emprestimo_id=emprestimo.id
    ).order_by(
        Parcela.numero.asc()
    ).all()

    return render_template(
        "parcelamento_detalhes.html",
        emprestimo=emprestimo,
        parcelas=parcelas
    )